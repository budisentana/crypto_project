import requests
import json
import timeit
import time
import os
import os.path
import sqlite3
from requests_toolbelt.multipart.encoder import MultipartEncoder


def upload_apk(FILE):
    print("Uploading file")
    multipart_data = MultipartEncoder(fields={'file': (FILE, open(FILE, 'rb'), 'application/octet-stream')})
    headers = {'Content-Type': multipart_data.content_type, 'Authorization': APIKEY}
    response = requests.post(SERVER + '/api/v1/upload', data=multipart_data, headers=headers)
    return response.content

def scan_apk(data):
    print("Scanning file")
    post_dict = json.loads(data)
    headers = {'Authorization': APIKEY}
    response = requests.post(SERVER + '/api/v1/scan', data=post_dict, headers=headers)
    return response.content

def json_resp(data):
    print("Generate JSON report")
    headers = {'Authorization': APIKEY}
    data = {"hash": json.loads(data)["hash"]}
    response = requests.post(SERVER + '/api/v1/report_json', data=data, headers=headers)
    return response.content

def delete(data):
    """Delete Scan Result"""
    print("Deleting Scan")
    headers = {'Authorization': APIKEY}
    data = {"hash": json.loads(data)["hash"]}
    response = requests.post(SERVER + '/api/v1/delete_scan', data=data, headers=headers)
    print(response.text)


SERVER = "http://127.0.0.1:8000"
APIKEY = '0e714b825e40876307cb27e0e48d0daf3606209d3d5aba53c39fdf6b16260a37'
apk_path = '/home/budi/crypto_project/apps_list/'
# apk_path = '/home/budi/OTP_project/apk_test/'
result_path = '/home/budi/crypto_project/crypto_code/mobsf_analysis/mobsf_result/'

for root, dirs, files  in os.walk(apk_path):
    for file in files:
        file_upload = root+ file.rstrip("\n")
        print(file_upload)
        res_upload = upload_apk(file_upload)
        scan_apk(res_upload)
  
        # access API for json report
        json_path = result_path+file.strip('\n')+'.json'
        print(json_path)
        json_res = json_resp(res_upload)
        to_dict = json.loads(json_res)
        with open (json_path,'w+') as jp:
            json.dump(to_dict,jp) 
    
        # don't touch this --> 
        # delete(res_upload)
        print(file + '-->saved')
        time.sleep(2)


