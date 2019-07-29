import os

import requests
import zipfile
import shutil

from dwf.common.config import deploy_config
from dwf.datapattern.metadata.image_folder4_classification import ImageFolder4Classfication
from dwf.datapattern.metadata.two_image_folder4_detection_txt import TwoImageFolder4Detection_txt

def upload_algorithm(algorithm_name, description, requirements=None, entrance=None, mirror=None, sample_dataset_path=None):
    kilobytes = 1024
    megabytes = kilobytes * 1000
    chunk_size = int(2 * megabytes)
    server_url = "http://192.168.35.59:30800/api/engine"
    filename = "/Users/sherry/GitHub/Xlearn-Algorithms/SSD/SSD.zip"

    part_num = 0
    input_file = open(filename, 'rb')
    real_name = os.path.basename(filename)
    headers = {
        'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NjQzOTI3NzMsImlhdCI6MTU2NDM4OTE3MywibmJmIjoxNTY0Mzg5MTczLCJ1c2VyX2lkIjoiVVNFUjQ0YzJmMDg3MTFlODhkNDkzNGUxMmRkMDdjMDciLCJ1c2VybmFtZSI6InhsZWFybiJ9.8Hk577Y4J8y50Qw6e4MAkyJjmbWFvvfPAVVFo0-QZXo"
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
        'train_input_pattern':patterns
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


def upload_dataset(dataset_name, description):
    kilobytes = 1024
    megabytes = kilobytes * 1000
    chunk_size = int(2 * megabytes)
    server_url = "http://192.168.35.59:30800/api/engine"
    filename = "/Users/sherry/Desktop/xlearn_data/jilv.zip"

    part_num = 0
    input_file = open(filename, 'rb')
    real_name = os.path.basename(filename)
    headers = {
        'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NjQzOTI3NzMsImlhdCI6MTU2NDM4OTE3MywibmJmIjoxNTY0Mzg5MTczLCJ1c2VyX2lkIjoiVVNFUjQ0YzJmMDg3MTFlODhkNDkzNGUxMmRkMDdjMDciLCJ1c2VybmFtZSI6InhsZWFybiJ9.8Hk577Y4J8y50Qw6e4MAkyJjmbWFvvfPAVVFo0-QZXo"
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
        'patterns': patterns
        # 'data_file_format': '',
        # 'user': 'USER44c2f08711e88d4934e12dd07c07',
        # 'username': 'xlearn'

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

# upload_dataset('jilv','ji lv')
# upload_algorithm(algorithm_name="SSD", \
#                  description="SSD", entrance='ssd_train.train')
