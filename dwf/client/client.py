import requests
import os
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


def upload_dataset(dataset_id, dataset_name, filename, server_url, description, visibility, owner):
    kilobytes = 1024
    megabytes = kilobytes * 1000
    chunk_size = int(2 * megabytes)
    # filename = "/Users/yangyucheng/Desktop/xlearn-data/xlearn-data1.zip"
    # server_url = "http://192.168.6.112:8888"

    part_num = 0
    input_file = open(filename, 'rb')
    real_name = os.path.basename(filename)
    headers = {
        #'token': deploy_config.get("CLUSTER", "TOKEN")
    }
    data = {
        'id': dataset_id,
        'name': dataset_name,
        'filename': real_name,
        'description': description,
        'visibility': visibility,
        'owner': owner,
        'user':'USER44c2f08711e88d4934e12dd07c07',
        'username':'xlearn'
    }
    response = requests.post(server_url + '/dataset/upload', data=data, headers=headers)
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
