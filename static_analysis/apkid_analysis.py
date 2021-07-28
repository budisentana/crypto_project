
import os
import json
import subprocess


apk_file = '/home/budi/crypto_project/sandbox/com.bitcoin.mwallet.apk'

def extract_APKID(apk_file):
    check_apk = 'apkid -v -r -j '+apk_file #+' >'+res
    res = subprocess.getoutput(check_apk)
    # print(res)
    return res

def find_package(apk_file):
    split_apk = apk_file.split('/')
    app_name = split_apk[-1]
    return app_name

def apkid_analysis(apk_file):
    # print(apk_file)
    app_name = find_package(apk_file)
    apkid_list=[]
    print('Extracting apps apkid : '+app_name)
    result = extract_APKID(apk_file)
    try:
        json_data = json.loads(result)
        pkg_key =  json_data['files']
        for item in pkg_key:
            class_dex = str(item['filename'])
            class_dex=class_dex.split('!')
            dex= str('!'.join(class_dex[1:])).strip('[]')
            for comp_type in item['matches']:
                # print(dex,comp_type,item['matches'][comp_type])
                matches = item['matches'][comp_type]
                apkid_list.append({'app_name':app_name,'class_dex':dex,'types':comp_type,'matches':matches})
    except:
        apkid_list.append({'app_name':app_name,'class_dex':'error','types':'error','matches':'error'})

    return(apkid_list)

def main():  
    apkid = apkid_analysis(apk_file)
    for line in apkid:
        print(line)

if __name__ == "__main__":
    main()
