import os

import requests

from dwf.common.config import deploy_config


def upload_algorithm(algo_id, server_url, filename, algorithm_name, description, requirements, entrance, mirror):
    kilobytes = 1024
    megabytes = kilobytes * 1000
    chunk_size = int(2 * megabytes)

    part_num = 0
    input_file = open(filename, 'rb')
    real_name = os.path.basename(filename)
    headers = {
        'token': deploy_config.get("CLUSTER", "TOKEN"),
    }
    data = {
        'id': algo_id,
        'name': algorithm_name,
        'description': description,
        'filename': real_name,
        'requirements': requirements,
        'entrance': entrance,
        'mirror': mirror,
        'visibility': 3,
        'usage': 3,
        'owner': deploy_config.get("CLUSTER", "OWNER"),
        'user':'USER44c2f08711e88d4934e12dd07c07',
        'username':'xlearn'
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
    filename = "/Users/Lanxiaozhi/0920crop.zip"

    part_num = 0
    input_file = open(filename, 'rb')
    real_name = os.path.basename(filename)
    headers = {
        'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NjM4NTUwNTgsImlhdCI6MTU2Mzg1MTQ1OCwibmJmIjoxNTYzODUxNDU4LCJ1c2VyX2lkIjoiVVNFUjQ0YzJmMDg3MTFlODhkNDkzNGUxMmRkMDdjMDciLCJ1c2VybmFtZSI6InhsZWFybiJ9.pxOaioX45W8L6fwaJtbtSd4XV2D2uuWrvOanqjvh9lg"
    }
    data = {
        'name': dataset_name,
        'datasource_id': 'DSOU30d2d78e6cb211e98f720a580af4',
        'description': description,
        'filename': real_name,
        # 'patterns': '',
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


upload_dataset(dataset_name='test_upload23', description='test')
