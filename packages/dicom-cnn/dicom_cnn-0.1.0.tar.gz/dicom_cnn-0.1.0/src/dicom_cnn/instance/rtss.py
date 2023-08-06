#TODO voir si on monte en abstraction avec des sous objects

class ROI:

    roi_dict :dict

    def __init__(self, roi_dict :dict) -> None:
        self.roi_dict = roi_dict
        pass
    
    def get_ROI_name(self, number_roi:int) -> str:
        return self.roi_dict['ROIName']

    def get_ROI_volume(self, number_roi:int) -> str:
        return self.roi_dict['ROIVolume']

    def get_ROI_generation_algorithm(self, number_roi:int) -> str :
        return self.roi_dict['ROIGenerationAlgorithm']