import numpy as np 
import scipy.ndimage
import imageio
from multiprocessing import Pool, cpu_count
import imageio.core.util
from PIL import Image
import io
from .utils import normalize_image

def silence_imageio_warning(*args, **kwargs):
    pass

class MIPGenerator:
    COLOR_TABLE = [
                (255, 0, 0, 100), # red
                (192, 192, 192, 100), # silver
                (128, 128, 128, 100), # gray
                (64, 64, 64, 100), # black
                (255, 255, 255, 100), # white
                (128, 0, 0, 100), # maroon
                (255, 255, 0, 100), # yellow
                (128, 128, 0, 100), # olive
                (0, 255, 0, 100), # lime
                (0, 128, 0, 100), # green
                (0, 255, 255, 100), # aqua
                (0, 128, 128, 100), # teal
                (0, 0, 255, 100), # blue
                (0, 0, 128, 100), # navy
                (255, 0, 255, 100), # fuchsia
                (128, 0, 128, 100), # purple
    ]

    """a class to generate MIP"""

    def __init__(self) -> None:
        """constructor

        Args:
            numpy_array (np.ndarray): [3D np.ndarray of shape (z,y,x) or 4D np.ndarray of shape (z,y,x,c)]
        """
        self.numpy_array = None
        self.frames = 24
        self.delay = 0.1
        self.max_rotation = 360
        self.nb_colors = 1
        self.projection_function = self.project_uncolored
        imageio.core.util._precision_warn = silence_imageio_warning

    def set_delay(self, delay: float) -> None:
        self.delay = delay

    def set_frames(self, frames: int) -> None:
        self.frames = frames

    def set_max_rotation(self, max_rotation: int) -> None:
        if (max_rotation < 0 or max_rotation > 360):
            raise("Out of bounds rotation")
        self.max_rotation = max_rotation

    def set_nb_colors(self, nb_colors: int) -> None:
        if (nb_colors < 0 or nb_colors > 16):
            raise("Out of bounds number of colors")
        self.nb_colors = nb_colors
        if (nb_colors == 0):
            self.projection_function = self.project_uncolored
        else:
            self.projection_function = self.project_colored

    def set_numpy_array(self, numpy_array: np.ndarray) -> None:
        self.numpy_array = numpy_array

    def set_colored(self, colored: bool) -> None:
        self.projection_function = self.project_colored if colored else self.project_uncolored

    def project_uncolored(self, angle:int) -> np.ndarray:
        """function to generate 2D MIP of a 3D (or 4D) ndarray of shape (z,y,x) (or shape (z,y,x,C)) 

        Args:
            angle (int): [angle of rotation of the MIP, 0 for coronal, 90 saggital ]

        Returns:
            [np.ndarray]: [return the MIP np.ndarray]
        """
        vol_angle = scipy.ndimage.rotate(
            self.numpy_array, angle=angle, reshape=False, axes=(2, 1), order=0, mode='constant', cval=0.0, prefilter=False)
        MIP = np.amax(vol_angle, axis=1)
        return MIP

    def project_colored(self, angle: int) -> np.ndarray:
        MIP = self.project_uncolored(angle)
        newData = []
        for item in np.nditer(MIP):
            if item != 0:
                color_index = int(item) % self.nb_colors
                newData.append(MIPGenerator.COLOR_TABLE[color_index])
            else:
                newData.append((255, 255, 255, 0))
        Image = np.array(newData).reshape(MIP.shape[0], MIP.shape[1], 4)
        return Image

    def get_projection_list(self) -> list:
        """Function to create a list of 2D MIP

        Returns:
            list: [list of 2D MIP]
        """
        angles = np.linspace(0, self.max_rotation, self.frames)
        nbCores = max(1, cpu_count() - 2)
        pool = Pool(nbCores)
        projection_list = pool.map(self.projection_function, angles)
        return projection_list

    def export_gif(self, output) -> None:
        """Function to create a gif from a 3D Array

        Args:
            output : [Where to save the gif]

        Returns:
            [None]: [None]
        """
        projection_list = self.get_projection_list()
        imageio.mimwrite(output, projection_list, format='.gif', duration=self.delay)

class MaskMIPGenerator:
    def __init__(self) -> None:
        self.numpy_array = None
        self.mask_array = None
        self.frames = 24
        self.delay = 0.1
        self.max_rotation = 360
        self.nb_colors = 16

    def set_numpy_array(self, numpy_array: np.ndarray) -> None:
        self.numpy_array = numpy_array

    def set_mask_array(self, mask_array: np.ndarray) -> None:
        self.mask_array = mask_array

    def set_nb_colors(self, nb_colors: int) -> None:
        if (nb_colors < 0 or nb_colors > 16):
            raise("Out of bounds number of colors")
        self.nb_colors = nb_colors

    def set_max_rotation(self, max_rotation: int) -> None:
        self.max_rotation = max_rotation
    
    def set_frames(self, frames: int) -> None:
        self.frames = frames

    def set_delay(self, delay: int) -> None:
        self.delay = delay

    def blend_np_arrays(self, background: np.ndarray, foreground: np.ndarray) -> np.ndarray:
        background_image = Image.fromarray(background.astype(np.uint8))
        foreground_image = Image.fromarray(foreground.astype(np.uint8))

        background_image = background_image.convert("RGBA")
        foreground_image = foreground_image.convert("RGBA")

        background_image.paste(foreground_image, (0, 0), foreground_image)
        return np.array(background_image)

    def get_projection_list(self):
        pet_arrays = []
        mask_arrays = []

        buffer = MIPGenerator()
        buffer.set_frames(self.frames)
        buffer.set_max_rotation(self.max_rotation)
        buffer.set_delay(self.delay)

        buffer.set_nb_colors(0)
        buffer.set_numpy_array(self.numpy_array)
        pet_arrays = buffer.get_projection_list()

        buffer.set_nb_colors(self.nb_colors)
        buffer.set_numpy_array(self.mask_array)
        mask_arrays = buffer.get_projection_list()

        projection_list = []
        for i in range(len(pet_arrays)):
            projection_list.append(self.blend_np_arrays(pet_arrays[i], mask_arrays[i]))
        return projection_list

    def export_gif(self, output) -> None:
        if (self.numpy_array is None or self.mask_array is None):
            raise("Nothing to export")
        if (self.numpy_array.shape != self.mask_array.shape):
            raise("Arrays are not the same shape")
        projection_list = self.get_projection_list()
        imageio.mimwrite(output, projection_list, format='.gif', duration=self.delay)