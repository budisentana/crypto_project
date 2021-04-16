import os 
import json

result_path = '/home/budi/OTP_project/OTP_code/mobsf_analysis/mobsf_result/'
split_apk_path = '/home/budi/OTP_project/OTP_code/mobsf_analysis/split_apk_list.txt'

split_apk_list=[]
for root,files,files in os.walk(result_path):
    for file in files:
        file_path = root+file
        print(file_path)
        with open (file_path,'r') as result_file:
            try:
                data = result_file.read()
                json_data = json.loads(data)
                check_split = json_data['app_name']
                print(check_split)
                if check_split == '':
                    split_apk_list.append(file)
            except:
                pass

with open(split_apk_path,'w') as split_file:
    for item in split_apk_list:
        split_file.write(item+'\n')