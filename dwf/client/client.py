import os

import requests
import zipfile
import shutil

from dwf.common.config import deploy_config
from dwf.datapattern.metadata.image_folder4_classification import ImageFolder4Classfication
from dwf.datapattern.metadata.two_image_folder4_detection_txt import TwoImageFolder4Detection_txt

def upload_algorithm(algo_id, server_url, filename, algorithm_name, description, requirements, entrance, mirror, sample_dataset_path):
    kilobytes = 1024
    megabytes = kilobytes * 1000
    chunk_size = int(2 * megabytes)

    part_num = 0
    input_file = open(filename, 'rb')
    real_name = os.path.basename(filename)
    headers = {
        'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NjM4NjI4OTUsImlhdCI6MTU2Mzg1OTI5NSwibmJmIjoxNTYzODU5Mjk1LCJ1c2VyX2lkIjoiVVNFUjQ0YzJmMDg3MTFlODhkNDkzNGUxMmRkMDdjMDciLCJ1c2VybmFtZSI6InhsZWFybiJ9.x-CgduDbYiWpiAJ_A0NCd3mjtuB5C6ZtUPwdxc-EoYM"
    }

    f = zipfile.ZipFile(sample_dataset_path,'r')
    for file in f.namelist():
        f.extract(file,"./tmp/")

    try:
        pattern = TwoImageFolder4Detection_txt()
        pattern.check('./tmp/')
        patterns = pattern.generate('./tmp')
    except:
        pass

    try:
        pattern = ImageFolder4Classfication()
        pattern.check('./tmp/')
        patterns = pattern.generate('./tmp')
    except:
        pass

    shutil.rmtree('./tmp/')

    data = {
        'name': algorithm_name,
        'description': description,
        # 'filename': real_name,
        # 'requirements': requirements,
        'entry_name': entrance,
        'train_input_pattern':patterns
        # 'mirror': mirror,
        # 'visibility': 3,
        # 'usage': 3,
        # 'owner': deploy_config.get("CLUSTER", "OWNER"),
    }
    response = requests.post(server_url + '/algorithm/upload', data=data, headers=headers)
    print(response.text)
    response = response.json()
    print("=" * 50)
    print(response)
    print("=" * 50)
    file_id = response['file_id']
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
        print("Response:", requests.post(server_url + '/upload', data=data, headers=headers, files=files).text)
        part_num += 1
    input_file.close()

    data = {
        'file_id': file_id,
    }
    print("Response:", requests.post(server_url + '/upload_finish', data=data, headers=headers).text)


def upload_dataset(dataset_name, description):
    kilobytes = 1024
    megabytes = kilobytes * 1000
    chunk_size = int(2 * megabytes)
    server_url = "http://192.168.10.22:30799/api/engine"
    filename = "/Users/sherry/Desktop/xlearn_data/0716.zip"

    part_num = 0
    input_file = open(filename, 'rb')
    real_name = os.path.basename(filename)
    headers = {
        'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NjM4NjI4OTUsImlhdCI6MTU2Mzg1OTI5NSwibmJmIjoxNTYzODU5Mjk1LCJ1c2VyX2lkIjoiVVNFUjQ0YzJmMDg3MTFlODhkNDkzNGUxMmRkMDdjMDciLCJ1c2VybmFtZSI6InhsZWFybiJ9.x-CgduDbYiWpiAJ_A0NCd3mjtuB5C6ZtUPwdxc-EoYM"
    }

    f = zipfile.ZipFile(filename,'r')
    for file in f.namelist():
        f.extract(file,"./tmp/")

    try:
        pattern = TwoImageFolder4Detection_txt()
        pattern.check('./tmp/')
        patterns = pattern.generate('./tmp')
    except:
        pass

    try:
        pattern = ImageFolder4Classfication()
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
    }
    response = requests.post(server_url + '/dataset/add', data=data, headers=headers)
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

upload_dataset('','')
