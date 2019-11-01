from dwf.datapattern.metadata.base_pattern import BasePattern
from dwf.common.exception import DATA_PATTERN_MISMATCH
from torchvision.datasets.folder import ImageFolder
import os
import cv2
from PIL import Image

class VideoBinFolder4Segmentation(BasePattern):
    def __init__(self):
        super(VideoBinFolder4Segmentation, self).__init__()
        self.data_type = 'video'
        self.organization = 'videoBinFolder4Segmentation'
        self.algos = 'unet'
        self.organization_parameter_width = None
        self.organization_parameter_height = None
        self.organization_parameter_channel = None
        self.organization_parameter_preprocess_resize_need = True
        self.organization_parameter_preprocess_resize_size = None
        self.organization_parameter_preprocess_crop_need = True
        self.organization_parameter_preprocess_crop_need = None
        self.organization_parameter_preprocess_shuffle_need = True
        self.organization_parameter_preprocess_normalization_need = True
        self.organization_parameter_preprocess_normalization_mean = None
        self.organization_parameter_preprocess_normalization_std = None

        self.semantic = '00'

    def check(self, folder_path):
        try:
            flash_path = os.path.join(folder_path, 'flash_data')
            grape_path = os.path.join(folder_path, 'grapes_data')

            if not os.path.exists(flash_path):
                raise DATA_PATTERN_MISMATCH

            if not os.path.exists(grape_path):
                raise DATA_PATTERN_MISMATCH

            # if len(image_list) != len(label_list):
            #     raise DATA_PATTERN_MISMATCH
            return True
        except:
            raise DATA_PATTERN_MISMATCH
        return True

    def generate(self, folder_path):
        return self.dumps()

    def generate_description(self):
        return 'binary data for severe weather'

# pattern = VideoFolder4Prediction()
# print(pattern.generate('/Users/sherry/Desktop/0920crop'))
# print(pattern.generate_description())

