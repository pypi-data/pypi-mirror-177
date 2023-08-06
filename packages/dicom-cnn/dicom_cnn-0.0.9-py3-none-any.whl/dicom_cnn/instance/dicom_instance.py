
from dataclasses import dataclass
from datetime import date, datetime

from matplotlib.pyplot import cla

from dicom_cnn.instance.tag_decorators import type_1, type_2, type_3
from .dicom_enums import CapturesSOPClass
import numpy as np


@dataclass
class DicomInstance():

    pixels :np.array = None
    manufacturer :str = None
    study_date :date = None
    study_time :datetime = None
    study_description :str = None
    series_description :str = None
    series_number :str = None
    patient_name :str = None
    patient_id :str = None
    patient_birthdate : str = None
    patient_sex :str = None
    patient_weight :float = None
    patient_size :float = None
    study_instance_uid :str = None
    sop_instance_uid :str = None
    series_instance_uid :str = None
    series_time :datetime = None
    series_date :datetime = None
    frame_of_reference_uid :str = None
    modality :str = None
    slice_thickness :float = None
    protocol_name :str = None
    acquisition_date :date = None
    acquisition_time :datetime = None
    columns :int = None
    rows :int = None
    content_date :date = None
    accession_number :str = None
    sop_class_uid :str = None
    pixel_spacing :list = None
    image_position :list = None
    image_orientation :list = None
    rescale_slope :float = None
    rescale_intercept :float = None


    @type_3
    def get_manufacturer(self) -> str:
        return self.manufacturer

    @type_2
    def get_study_date(self) -> date:
        return self.study_date

    @type_2
    def get_study_time(self) -> datetime:
        return self.study_time

    @type_3
    def get_study_description(self) -> str:
        return self.study_description

    @type_3
    def get_series_description(self) -> str:
        return self.series_description

    @type_2
    def get_series_number(self) -> str:
        return self.series_number

    @type_2
    def get_patient_name(self) -> str:
        return self.patient_name

    @type_2
    def get_patient_id(self) -> str:
        return self.patient_id

    @type_2
    def get_patient_birthdate(self) -> date:
        return self.patient_birthdate

    @type_3
    def get_patient_sex(self) -> str:
        return self.patient_sex

    @type_3
    def get_patient_weight(self) -> float:
        return self.patient_weight

    @type_3
    def get_patient_size(self) -> float:
        return self.patient_size

    @type_1
    def get_study_instance_uid(self) -> str:
        return self.study_instance_uid

    @type_1
    def get_sop_instance_uid(self) -> str:
        return self.sop_instance_uid

    def get_series_instance_uid(self) -> str:
        return self.series_instance_uid

    @type_3
    def get_series_time(self) -> datetime:
        return self.series_time

    @type_3
    def get_series_date(self) -> datetime:
        return self.series_date

    @type_1
    def get_frame_of_reference_uid(self) -> str:
        return self.frame_of_reference_uid

    @type_1
    def get_modality(self) -> str:
        return self.modality

    @type_2
    def get_slice_thickness(self) -> float:
        return self.slice_thickness

    @type_3
    def get_protocol_name(self) -> str:
        return self.protocol_name

    @type_3
    def get_acquisition_date(self) -> date:
        return self.acquisition_date

    @type_3
    def get_acquisition_time(self) -> datetime:
        return self.acquisition_time

    @type_1
    def get_columns(self) -> int:
        return self.columns

    @type_1
    def get_rows(self) -> int:
        return self.rows

    @type_1
    def get_content_date(self) -> date:
        return self.content_date

    @type_2
    def get_accession_number(self) -> str:
        return self.accession_number

    @type_1
    def get_sop_class_uid(self) -> str:
        return self.sop_class_uid

    @type_1
    def get_series_instance_uid(self) -> str:
        return self.series_instance_uid

    @type_1
    def get_pixel_spacing(self) -> list:
        return self.pixel_spacing

    @type_1
    def get_image_position(self) -> list:
        return self.image_position

    def get_image_orientation(self) -> list:
        return self.image_orientation

    @type_1
    def get_rescale_slope(self) -> float:
        return self.rescale_slope


    @type_1
    def get_rescale_intercept(self) -> float:
        return self.rescale_intercept

    @classmethod  
    def parse_dicom_date(cls, dicom_date: str) -> date:      
        return datetime.strptime(dicom_date, '%Y%m%d').date()

    @classmethod
    def parse_dicom_time(cls, dicom_time: str) -> datetime:
        """Parse DICOM Time values to generate a time object

        Args:
            dicom_time (str): DICOM Time String (HHMMSS.FFFFFF)

        Returns:
            time: time value
        """

        if ("." not in dicom_time):
            dicom_time = dicom_time+".000000"

        return datetime.strptime(dicom_time, '%H%M%S.%f').time()

    @classmethod
    def parse_dicom_datetime(self, dicom_datetime :str) ->datetime:
        if ("." not in dicom_datetime):
            dicom_datetime = dicom_datetime+".000000"
        return datetime.strptime(dicom_datetime, '%Y%m%d%H%M%S.%f')

    def is_secondary_capture(self) -> bool:
        """check if SOPClassUID in CapturesSOPClass list
        Returns:
            [bool]: [return True if SOPCLassUID in CapturesSOPClass list, False instead]
        """
        capture_sop_list = list(
            map(lambda x: x.value, CapturesSOPClass._member_map_.values()))
        return True if self.sop_class_uid in capture_sop_list else False

    def get_image_nparray(self) -> np.ndarray:
        """get instance image ndarray (taking account rescale slope and intercept)
        Returns:
            [ndarray]: [return instance image ndarray]
        """
        pixel_array = self.pixels
        rescale_slope = self.get_rescale_slope()
        rescale_intercept = self.get_rescale_intercept()

        resultArray = (pixel_array * rescale_slope) + rescale_intercept
        return resultArray

@dataclass
class DicomInstancePT(DicomInstance):

    radiopharmaceutical_start_time :datetime = None
    radiopharmaceutical_start_datetime :datetime = None
    radiopharmaceutical_stop_time :datetime = None
    radionuclide_totale_dose :str = None
    radionuclide_half_life :float = None
    correction_image :list = None
    philips_suv_factor :float = None
    philips_bqml_factor :float = None
    units :str = None
    decay_correction :str = None

    @type_3
    def get_radiopharmaceutical_start_time (self) -> datetime:
        return self.radiopharmaceutical_start_time

    @type_3
    def get_radiopharmaceutical_start_datetime (self) -> datetime:
        return self.radiopharmaceutical_start_datetime
    
    @type_3
    def get_radiopharmaceutical_stop_time (self) -> datetime:
        return self.radiopharmaceutical_stop_time
    
    @type_3
    def get_radionuclide_total_dose (self) -> str:
        return self.radionuclide_totale_dose

    @type_3
    def get_radionuclide_half_life (self) -> float:
        return self.radionuclide_half_life
    
    @type_3
    def get_correction_image (self)-> list:
        return self.correction_image

    @type_3
    def get_philips_suv_factor(self) -> float:
        return self.philips_suv_factor 

    @type_3
    def get_philips_bqml_factor(self) -> float:
        return self.philips_bqml_factor 

    @type_1
    def get_units (self) -> str:
        return self.units
        
    @type_1
    def get_decay_correction (self)-> str:
        return self.decay_correction

@dataclass
class DicomInstanceRTDose(DicomInstance):

    dvh_sequence :list = None

    @type_3
    def get_dvh_sequence(self) -> list:
        return self.dvh_sequence

    def get_image_nparray(self) -> np.ndarray:
        """get instance image ndarray, no rescale slope intercept for RTDose
        Returns:
            [ndarray]: [return instance image ndarray]
        """
        pixel_array = self.pixels
        return pixel_array

class DicomInstanceRTSS(DicomInstance):

    structure_set_roi_sequence :list = None
    roi_contour_sequence :list = None
    frame_of_reference_sequence :list = None

    def get_image_nparray(self):
        raise('Cannot get image numpy array from RTSTRUCT FILE')

    def get_number_of_roi(self) -> int:
        return len(self.structure_set_roi_sequence)

    def get_ROI(self, number_roi :int) -> dict:
        return self.structure_set_roi_sequence[number_roi - 1]

    def get_ROI_name(self, number_roi:int) -> str:
        return self.get_ROI(number_roi)['ROIName']

    def get_ROI_volume(self, number_roi:int) -> str:
        return self.get_ROI(number_roi)['ROIVolume']

    def get_ROI_generation_algorithm(self, number_roi:int) -> str :
        return self.get_ROI(number_roi)['ROIGenerationAlgorithm']

    #info from ReferencedFrameOfReferenceSequence
    def get_number_of_frame_of_reference(self) -> int:
        """method to count the series referenced in ReferencedFrameOfReference Sequence
        """
        return len(self.frame_of_reference_sequence)

    def get_frame_of_reference_uids(self) -> list:
        """method to get FrameOfReferenceUID for each series referenced in ReferencedFrameOfReference Sequence.
            Usually, only one serie referenced.
        """
        list = []
        for frame_of_reference in self.frame_of_reference_sequence:
            list.append(frame_of_reference['FrameOfReferenceUID'])
        return list 

    def is_same_frame_of_reference(self) -> bool:
        """check if all FrameOfReferenceUID in RTSS are identical
        """
        frame_of_reference_uids = self.get_frame_of_reference_uids()
        unique_value = list(set(frame_of_reference_uids))
        return True if len(unique_value) == 1 else False 

    def get_list_all_SOP_Instance_UID_RTSS(self) -> list:
        """method to get all SOPInstanceUID referenced in RTSTRUCT File

        Returns:
            [list]: [list of all SOP Instance UID]
        """
        number_item = len(self.dicomData[0x30060010][0].RTReferencedStudySequence[0].RTReferencedSeriesSequence[0].ContourImageSequence)
        liste = []
        for i in range(number_item):
            liste.append(str(self.dicomData[0x30060010][0].RTReferencedStudySequence[0].RTReferencedSeriesSequence[0].ContourImageSequence[i].ReferencedSOPInstanceUID))
        return liste

    def get_referenced_series_instance_uid(self) -> list:
        """method to get a list of SeriesInstanceUID for each series referenced in ReferencedFrameOfReference Sequence.
            Usually, only one serie referenced.
            Has to be the same SeriesInstanceUID in the associated serie. 

        Returns:
            [list]: [list of SeriesInstanceUID for each series referenced]
        """
        number_serie = len(self.dicomData.ReferencedFrameOfReferenceSequence)
        liste = []
        for i in range(number_serie):
            liste.append(self.dicomData[0x30060010][i].RTReferencedStudySequence[0].RTReferencedSeriesSequence[0].SeriesInstanceUID)
        return liste


    def get_referenced_study_SOP_instance_uid(self) -> list :
        """method to get a list of StudyInstanceUID for each series referenced in ReferencedFrameOfReference Sequence.
            Usually, only one serie referenced.
            Has to be the same StudyInstanceUID in the associated serie. 

        Returns:
            [list]: [list of StudyInstanceUID for each series referenced]
        """
        number_serie = len(self.dicomData.ReferencedFrameOfReferenceSequence)
        liste = []
        for i in range(number_serie):
            liste.append(self.dicomData[0x30060010][i].RTReferencedStudySequence[0].ReferencedSOPInstanceUID)
        return liste


    def get_referenced_SOP_class_UID(self) -> list :
        """method to get a list of SOPClassUID for each series referenced in ReferencedFrameOfReference Sequence.
            Usually, only one serie referenced.
            Has to be the same SOPCLassUID in the associated serie. 

        Returns:
            [list]: [list of SOPClassUID for each series referenced]
        """
        number_serie = len(self.dicomData.ReferencedFrameOfReferenceSequence)
        liste = []
        for i in range(number_serie):
            liste.append(self.dicomData[0x30060010][i].RTReferencedStudySequence[0].RTReferencedSeriesSequence[0].ContourImageSequence[0].ReferencedSOPClassUID)
        return liste 

    #info from ROIContourSequence
    def get_roi_display_color(self, number_roi:int) -> str :
        """method to get ROI color representation from ROIContour Sequence

        Args:
            number_roi (int): [ROI number; start at 1. ]

        Returns:
            [str]: [return ROIDisplayColor value , format [r,g,b]]
        """
        return self.roi_contour_sequence[number_roi - 1].ROIDisplayColor 


    def get_list_contour_SOP_Instance_UID(self, roi_number:int) -> list: 
        """method to get a list of every contour SOPINstanceUID  from ROIContour Sequence

        Args:
            number_roi (int): [ROI number; start at 1. ]

        Returns:
            [list]: [return list of every SOPInstanceUID where there is a contour]
        """
        number_item = len(self.dicomData[0x30060039][roi_number - 1].ContourSequence)
        liste = []
        for i in range(number_item):
            liste.append(str(self.dicomData[0x30060039][roi_number - 1].ContourSequence[i].ContourImageSequence[0].ReferencedSOPInstanceUID))
        return liste 

    
    def is_referenced_SOP_Instance_UID_in_all_SOP_Instance(self) -> bool :
        """check if every  SOPInstanceUID contour is referenced in the SOPINstanceUID of the associated serie

        Raises:
            Exception: [Exception if one of the SOPInstanceUID contour is not referenced in all SOPInstanceUID of the associated serie]

        Returns:
            [bool]: [True if everything referenced, raise Exception instead]
        """
        all_sop = str(self.get_list_all_SOP_Instance_UID_RTSS)
        referenced_sop = str(self.get_list_contour_SOP_Instance_UID)
        for uid in referenced_sop : 
            if uid not in all_sop : 
                raise Exception("SOP Instance UID not in the serie")
        return True 


    def get_number_of_contour_points(self, roi_number:int) -> list:
        """method to get a list of every NumberOfContourPoint in each contours  from ROIContour Sequence

        Args:
            number_roi (int): [ROI number; start at 1. ]

        Returns:
            [list]: [return list of number of contour points]
        """
        number_item = len(self.dicomData[0x30060039][roi_number - 1].ContourSequence)
        liste = []
        for i in range(number_item):
            liste.append(self.dicomData[0x30060039][roi_number - 1].ContourSequence[i].NumberOfContourPoints)
        return liste

    def get_list_contour_geometric_type(self, roi_number:int) -> list :
        """method to get a list of every ContourGeomtricType value of each contour  from ROIContour Sequence

        Args:
            number_roi (int): [ROI number; start at 1. ]

        Returns:
            [list]: [return a list with every ContourGeometricType value for each contour]
        """
        number_item = len(self.dicomData[0x30060039][roi_number - 1].ContourSequence)
        liste = []
        for i in range(number_item):
            liste.append(self.dicomData[0x30060039][roi_number - 1].ContourSequence[i].ContourGeometricType)
        return liste

    def is_closed_planar(self, roi_number:int) -> bool :
        """check if every contour is CLOSED_PLANAR  from ROIContour Sequence

        Args:
            roi_number (int): [ROI number, start a 1]

        Returns:
            [bool]: [return True if every value is CLOSED_PLANAR, False instead]
        """
        geometric_type = self.get_list_contour_geometric_type(roi_number)
        for type in geometric_type :
            if type != "CLOSED_PLANAR" : 
                return False
        return True 

    def get_contour_data(self, roi_number:int) -> list :
        """method to get contour data of contours  from ROIContour Sequence

        Args:
            number_roi (int): [ROI number; start at 1. ]

        Returns:
            [list]: [return list of contour data for each contour [[contour1 : x, y, z, x, y ,z, ...], [contour2 : ...], [...]] ]
        """
        number_item = len(self.dicomData[0x30060039][roi_number - 1].ContourSequence)
        liste = []
        for i in range(number_item):
            liste.append(self.dicomData[0x30060039][roi_number - 1].ContourSequence[i].ContourData)
        return liste 

