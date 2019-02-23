#
# DataWay Dataset SDK
# Author: peizhongyi(peizhyi@gmail.com)
# Initial Date: 2018.06.20
#
# Title: Format Definition of Dataset
#
# Version 0.1
#

import json


class VideoFormat:
    def __init__(self, weight, height, channel):
        self.weight = weight 
        self.height = height
        self.channel = channel

    def __repr__(self):
        return 'Screen size(weight * height): %s * %s, Channel: %s' % (self.weight, self.height, self.channel)

    @staticmethod
    def _object_decoder(obj):
        return VideoFormat(obj['weight'], obj['height'], obj['channel'])

    @staticmethod
    def parse(config_json):
        return json.loads(config_json, object_hook=VideoFormat._object_decoder)


class ImageFormat:
    def __init__(self, image_size, channel, num_classes):
        self.image_size = image_size
        self.channel = channel
        self.num_classes = num_classes

    def __repr__(self):
        return 'Image size: %s, Channel: %s, Num Classes: %s' % (self.image_size, self.channel, self.num_classes)

    @staticmethod
    def _object_decoder(obj):
        return ImageFormat(obj['image_size'], obj['channel'], obj['num_classes'])

    @staticmethod
    def parse(config_json):
        return json.loads(config_json, object_hook=ImageFormat._object_decoder)

