from dwf.datapattern.metadata.base_pattern import BasePattern
from dwf.common.exception import DATA_PATTERN_MISMATCH
from torchvision.datasets.folder import ImageFolder
import os
import cv2
from PIL import Image

class VideoFolder4Prediction(BasePattern):
    def __init__(self):
        super(VideoFolder4Prediction, self).__init__()
        self.data_type = 'video'
        self.organization = 'videoFolder4Prediction'
        self.algos = 'predrnn'
        self.organization_parameter_width = None
        self.organization_parameter_height = None
        self.organization_parameter_channel = None
        self.organization_parameter_preprocess_resize_need = True
        self.organization_parameter_preprocess_resize_size = 224
        self.organization_parameter_preprocess_crop_need = True
        self.organization_parameter_preprocess_crop_need = 256
        self.organization_parameter_preprocess_shuffle_need = True
        self.organization_parameter_preprocess_normalization_need = True
        self.organization_parameter_preprocess_normalization_mean = [0.5, 0.5, 0.5]
        self.organization_parameter_preprocess_normalization_std = [0.5, 0.5, 0.5]

        self.semantic = '00'

    def check(self, folder_path):
        try:
            dataset_pending = ImageFolder(root=folder_path)
        except:
            raise DATA_PATTERN_MISMATCH
        return True

    def generate(self, folder_path):
        max_width = 0
        min_width = 10000
        max_height = 0
        min_height = 10000
        channel_num = None
        for sub_dir in os.listdir(folder_path):
            for file in os.listdir(os.path.join(folder_path, sub_dir)):
                im = cv2.imread(os.path.join(folder_path, sub_dir,file))
                width, height, channel = im.shape[0],im.shape[1],im.shape[2]
                if channel_num is None:
                    channel_num = channel
                if channel != channel_num:
                    raise DATA_PATTERN_MISMATCH
                max_width = max(max_width, width)
                min_width = min(min_width, width)
                max_height = max(max_height, height)
                min_height = min(min_height, height)

        self.organization_parameter_width = [min_width, max_width]
        self.organization_parameter_height = [min_height, max_height]
        self.organization_parameter_channel = channel_num
        return self.dumps()

    def generate_description(self):
        if self.organization_parameter_channel == 3:
            image_type = 'RGB'
        else:
            # description_str = 'gray images with detection information in txt file'
            image_type = 'gray'
        description_str = image_type + ' ' + self.data_type + ' ' + 'in' + ' ' + self.organization
        return description_str

# pattern = VideoFolder4Prediction()
# print(pattern.generate('/Users/sherry/Desktop/0920crop'))
# print(pattern.generate_description())

