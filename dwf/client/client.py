import os

import requests
import zipfile
import shutil

from dwf.common.config import deploy_config
from dwf.datapattern.metadata.image_folder4_classification import ImageFolder4Classfication
from dwf.datapattern.metadata.two_image_folder4_detection_txt import TwoImageFolder4Detection_txt

def upload_algorithm(server_url, filename, algorithm_name, description, requirements=None, entrance=None, mirror=None, sample_dataset_path=None):
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
    patterns = ''
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
        'train_input_pattern':patterns,
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


def upload_dataset(server_url, filename, dataset_name, description):
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

    try:
        pattern = TwoImageFolder4Detection_txt()
        pattern.check('./tmp/')
        patterns = pattern.generate('./tmp')
    except:
        pass

    # try:
    #     pattern = ImageFolder4Classfication()
    #     pattern.check('./tmp/')
    #     patterns = pattern.generate('./tmp')
    # except:
    #     pass

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

# upload_dataset(server_url = "http://192.168.10.22:30800/api/engine", \
#                filename = "/Users/sherry/Desktop/xlearn_data/resnet_data/bucket_test.zip", \
#                dataset_name='满斗分类测试集', \
#                description='满斗测试集')

# upload_algorithm(server_url = "http://192.168.10.22:30800/api/engine", \
#                  filename = "/Users/sherry/GitHub/Xlearn-Algorithms/ResNet.zip", \
#                  algorithm_name="ResNet-Latest", \
#                  description="ResNet", \
#                  entrance='')

upload_model(server_url = "http://192.168.111.25:30800/api/engine", \
            filename = "/Users/sherry/Desktop/grease_cla_2500.pkl", \
            model_name='黄油枪分类模型(新)', \
            output_data_pattern='', \
            input_data_patern='resnet',
            algorithm_id='ALGOfd938eeeb21711e9aecf0a580af4',
            description='黄油枪分类模型')
