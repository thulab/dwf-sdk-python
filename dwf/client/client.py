import os

import requests
import zipfile
import shutil

from dwf.common.config import deploy_config
from dwf.datapattern.metadata.image_folder4_classification import ImageFolder4Classfication
from dwf.datapattern.metadata.two_image_folder4_detection_txt import TwoImageFolder4Detection_txt
from dwf.datapattern.metadata.video_folder4_prediction import VideoFolder4Prediction
from dwf.datapattern.metadata.video_bin_folder4_segmentation import VideoBinFolder4Segmentation


def upload_algorithm(server_url, filename, algorithm_name, description, train_input_pattern=None, model_input_pattern=None, \
                     hyperparameter_config=None, requirements=None, entrance=None, mirror=None, sample_dataset_path=None, learning=1):
    kilobytes = 1024
    megabytes = kilobytes * 1000
    chunk_size = int(2 * megabytes)
    # server_url = "http://192.168.35.59:30800/api/engine"
    # filename = "/Users/sherry/GitHub/Xlearn-Algorithms/ResNet/ResNet.zip"

    part_num = 0
    input_file = open(filename, 'rb')
    real_name = os.path.basename(filename)
    headers = {
        'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NjQ0MDg1NjcsIm5iZiI6MTU2NDQwODU2NywidXNlcl9pZCI6IlVTRVI0NGMyZjA4NzExZTg4ZDQ5MzRlMTJkZDA3YzA3IiwidXNlcm5hbWUiOiJ4bGVhcm4ifQ.75rPfxqIagzWtPemfX0NGTPoxqRhBJUC0PTp-YSdgGU"
    }
    # if sample_dataset_path is not None:
    #     f = zipfile.ZipFile(sample_dataset_path,'r')
    #     for file in f.namelist():
    #         f.extract(file,"./tmp/")
    #
    #     try:
    #         pattern = TwoImageFolder4Detection_txt()
    #         pattern.check('./tmp/')
    #         patterns = pattern.generate('./tmp')
    #     except:
    #         pass
    #
    #     try:
    #         pattern = ImageFolder4Classfication()
    #         pattern.check('./tmp/')
    #         patterns = pattern.generate('./tmp')
    #     except:
    #         pass
    #
    #     shutil.rmtree('./tmp/')

    data = {
        'name': algorithm_name,
        'description': description,
        'filename': real_name,
        # 'requirements': requirements,
        'entry_name': entrance,
        'hyperparameter_config': hyperparameter_config,
        'train_input_pattern':train_input_pattern,
        'train_output_pattern':'{}',
        'model_input_pattern': model_input_pattern,
        'model_output_pattern': '{}',
        'learning': learning,
        'available': 1,
        'user': 'USER44c2f08711e88d4934e12dd07c07',
        'username': 'xlearn'
        # 'mirror': mirror,
        # 'visibility': 3,
        # 'usage': 3,
        # 'owner': deploy_config.get("CLUSTER", "OWNER"),
    }
    response = requests.post(server_url + '/algorithm/add', data=data, headers=headers)
    print(response)
    response = response.json()
    print("=" * 50)
    print(response)
    print("=" * 50)
    file_id = response['data']
    while True:
        chunk = input_file.read(chunk_size)
        if not chunk:
            break
        files = {
            'file': chunk,
        }
        data = {
            'file_id': file_id,
            'chunk': part_num,
        }
        print("Uploading chunk %d:" % part_num)
        print("Response:", requests.post(server_url + '/algorithm/upload', data=data, headers=headers, files=files).text)
        part_num += 1
    input_file.close()

    data = {
        'file_id': file_id,
    }
    print("Response:", requests.post(server_url + '/algorithm/upload_finish', data=data, headers=headers).text)


def upload_dataset(server_url, data_type, filename, dataset_name, description):
    kilobytes = 1024
    megabytes = kilobytes * 1000
    chunk_size = int(2 * megabytes)
    # server_url = "http://192.168.35.59:30800/api/engine"
    # filename = "/Users/sherry/Desktop/xlearn_data/jilv.zip"

    part_num = 0
    input_file = open(filename, 'rb')
    real_name = os.path.basename(filename)
    headers = {
        'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NjQ0MDg1NjcsIm5iZiI6MTU2NDQwODU2NywidXNlcl9pZCI6IlVTRVI0NGMyZjA4NzExZTg4ZDQ5MzRlMTJkZDA3YzA3IiwidXNlcm5hbWUiOiJ4bGVhcm4ifQ.75rPfxqIagzWtPemfX0NGTPoxqRhBJUC0PTp-YSdgGU"
    }
    patterns = ''

    f = zipfile.ZipFile(filename,'r')
    for file in f.namelist():
        f.extract(file,"./tmp/")

    if data_type == 'image':
        try:
            pattern = TwoImageFolder4Detection_txt()
            pattern.check('./tmp/')
            patterns = pattern.generate('./tmp')
        except:
            try:
                pattern = ImageFolder4Classfication()
                pattern.check('./tmp/')
                patterns = pattern.generate('./tmp')
            except:
                pass


    else:
        try:
            pattern = VideoFolder4Prediction()
            pattern.check('./tmp/')
            patterns = pattern.generate('./tmp')
        except:
            try:
                pattern = VideoBinFolder4Segmentation()
                pattern.check('./tmp/')
                patterns = pattern.generate('./tmp')
            except:
                pass

    shutil.rmtree('./tmp/')

    data = {
        'name': dataset_name,
        'datasource_id': 'DSOU30d2d78e6cb211e98f720a580af4',
        'description': description,
        'filename': real_name,
        'patterns': patterns,
        # 'data_file_format': '',
        'user': 'USER44c2f08711e88d4934e12dd07c07',
        'username': 'xlearn'

    }
    response = requests.post(server_url + '/dataset/add', data=data, headers=headers)
    print(response)
    response = response.json()
    print("=" * 50)
    print(response)
    print("=" * 50)
    file_id = response['data']
    while True:
        chunk = input_file.read(chunk_size)
        if not chunk:
            break
        files = {
            'file': chunk,
        }
        data = {
            'file_id': file_id,
            'chunk': part_num,
        }
        print("Uploading chunk %d:" % part_num)
        print("Response:", requests.post(server_url + '/dataset/upload', data=data, headers=headers, files=files).text)
        part_num += 1
    input_file.close()

    data = {
        'file_id': file_id,
    }
    print("Response:", requests.post(server_url + '/dataset/upload_finish', data=data, headers=headers).text)

def upload_model(server_url, filename, model_name, output_data_pattern, input_data_patern, algorithm_id, description):
    kilobytes = 1024
    megabytes = kilobytes * 1000
    chunk_size = int(2 * megabytes)
    # server_url = "http://192.168.35.59:30800/api/engine"
    # filename = "/Users/sherry/Desktop/xlearn_data/jilv.zip"

    part_num = 0
    input_file = open(filename, 'rb')
    real_name = os.path.basename(filename)
    headers = {
        'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NjQ0MDg1NjcsIm5iZiI6MTU2NDQwODU2NywidXNlcl9pZCI6IlVTRVI0NGMyZjA4NzExZTg4ZDQ5MzRlMTJkZDA3YzA3IiwidXNlcm5hbWUiOiJ4bGVhcm4ifQ.75rPfxqIagzWtPemfX0NGTPoxqRhBJUC0PTp-YSdgGU"
    }

    data = {
        'name': model_name,
        'description': description,
        'filename': real_name,
        'output_data_patterns':output_data_pattern,
        'input_data_patterns':input_data_patern,
        'algorithm_id':algorithm_id
        # 'data_file_format': '',
        # 'user': 'USER44c2f08711e88d4934e12dd07c07',
        # 'username': 'xlearn'

    }
    response = requests.post(server_url + '/model/add', data=data, headers=headers)
    print(response)
    response = response.json()
    print("=" * 50)
    print(response)
    print("=" * 50)
    file_id = response['data']
    while True:
        chunk = input_file.read(chunk_size)
        if not chunk:
            break
        files = {
            'file': chunk,
        }
        data = {
            'file_id': file_id,
            'chunk': part_num,
        }
        print("Uploading chunk %d:" % part_num)
        print("Response:", requests.post(server_url + '/model/upload', data=data, headers=headers, files=files).text)
        part_num += 1
    input_file.close()

    data = {
        'file_id': file_id,
    }
    print("Response:", requests.post(server_url + '/model/upload_finish', data=data, headers=headers).text)

upload_dataset(server_url = "http://10.20.90.24:30800/api/engine", \
               data_type='video',\
               filename = "/Users/sherry/Desktop/guangzhou_all/201710.zip", \
               dataset_name='2017年10月', \
               description='2017年10月雷达外推数据')

upload_algorithm(server_url = "http://10.20.90.24:30800/api/engine", \
                 filename = "/Users/sherry/GitHub/Xlearn-Algorithms/PredRNN.zip", \
                 algorithm_name="PredRNN", \
                 description="PredRNN视频预测算法", \
                 entrance='predrnn_train_weather.train',
                 train_input_pattern='{"data_type": "video", "organization": "videoFolder4Prediction", "algos": "predrnn", "organization_parameter_width": [224, 224], "organization_parameter_height": [224, 224], "organization_parameter_channel": 3, "organization_parameter_preprocess_resize_need": true, "organization_parameter_preprocess_resize_size": 224, "organization_parameter_preprocess_crop_need": 256, "organization_parameter_preprocess_shuffle_need": true, "organization_parameter_preprocess_normalization_need": true, "organization_parameter_preprocess_normalization_mean": [0.5, 0.5, 0.5], "organization_parameter_preprocess_normalization_std": [0.5, 0.5, 0.5], "semantic": "00"}',
                 model_input_pattern='predrnn',
                 hyperparameter_config='[{"name": "patch_size", "type": "int", "default": 4, "alias":"patch size","scope":"<1,16>", "description":"片(Patch)的大小","suggest":1}, {"name": "lr", "type": "float", "default": 0.001, "alias":"learning rate", "scope":"<1e-4,1.0>", "description":"学习率大小","suggest":1}, {"name": "batch_size", "type": "int", "default": 1, "alias":"batch size","scope":"<1,64>", "description":"批(Batch)的大小","suggest":1},{"name": "max_iterations", "type": "int", "default": 80, "alias":"max iteration", "scope":"<80,8000>", "description":"总迭代次数","suggest":1}, {"name": "dataset1", "type": "radio", "alias":"训练数据集"}, {"name": "dataset2", "type": "radio", "alias":"验证数据集"}]')

# upload_model(server_url = "http://192.168.111.25:30800/api/engine", \
#             filename = "/Users/sherry/Desktop/grease_cla_2500.pkl", \
#             model_name='黄油枪分类模型(新)', \
#             output_data_pattern='', \
#             input_data_patern='resnet',
#             algorithm_id='ALGOfd938eeeb21711e9aecf0a580af4',
#             description='黄油枪分类模型')
