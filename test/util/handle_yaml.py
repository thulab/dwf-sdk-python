
# coding: utf-8


import yaml
import os


class HandleYaml:
    def __init__(self, file_path=None):
        if file_path:
            root_dir = os.path.abspath('.')
            self.file_path = file_path
            self.file_path = root_dir +"/test/data/"+self.file_path
        else:
            # root_dir = os.path.dirname(os.path.abspath('.'))
            root_dir = os.path.abspath('.')
            # print("abspath==============" + os.path.abspath('.'))
            # print("root_dir=============="+root_dir)
            # os.path.abspath('.')表示获取当前文件所在目录；os.path.dirname表示获取文件所在父目录；所以整个就是项目的所在路径
            self.file_path = root_dir + '/test/data/model_data.yaml'  # 获取文件所在的相对路径(相对整个项目)
        # self.data = self.get_data()

    def get_data(self):
        # print("-----------------------"+self.file_path)
        fp = open(self.file_path, encoding='utf-8')
        data = yaml.safe_load(fp)
        return data


if __name__ == '__main__':
    test = HandleYaml()
    p = test.get_data()
    print(p['add'])

