import json

class BasePattern(object):

    def __init__(self):
        pass

    def dumps(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def load(self, json_str):
        self.__dict__ = json.loads(json_str)

    def check(self, folder_path):
        raise NotImplementedError

    def generate(self, folder_path):
        raise NotImplementedError

    def generate_description(self):
        pass

