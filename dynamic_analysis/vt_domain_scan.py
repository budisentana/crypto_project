import os,json
import random
import hashlib
import requests


apk_path='/home/budi/crypto_project/apps_list/im.token.app.apk'
result_path = '/home/budi/crypto_project/vt_result/africa.bundle.mobile.app'

def random_key():
    vt_key = ['1162652624083e2616b2200d64c68d4ae92722b952c88418d46e46c14383ccae']#,
            # '5870a8e7b98608a0889e1b436341391bc47a956db1f7a5314686b7abad618376', # Tham's key
            # '3c189a9b3e6e8c2a0aba160aa1c0c0574ae56fcd5b264ee7856508d96f56095a'] # Budi's key

    key = random.choice(vt_key)
    return key



def vt_find_positive(result_path):
    vt_positive = []
    with open (result_path,'r') as rs:
        try:
            data = rs.read()
            json_data = json.loads(data)
            json_VT = json_data['scans']
            for item in json_VT:
                if json_VT[item]['detected'] == True:
                    # print(item,json_VT[item]['result'])
                    vt_positive.append({'engine':item,'malware':json_VT[item]['result']})
        except:
            # print('virus total error --------------------------------'+file)
            # item_list = {'path':app_file_path,'file':file}
            # app_to_analyze.append(item_list)
            pass
    return vt_positive

def search_vt_domain(domain):
    vt_url = 'https://www.virustotal.com/vtapi/v2/domain/report'
    vt_key = random_key()
    params = {'apikey': vt_key, 'domain':domain}
    print('Find VT report for '+domain)
    print('VT key '+vt_key)

    try:
        response = requests.get(vt_url, params=params)
        print('this is response '+response)
    except :
        print("Couldn't get response from virustotal")
    # print(response)
    try:
        js = response.json()
    except:
        print('Failed to convert respon to json')
        js = 'error'
    
    return js


def main():
    
    domain = 'www.pullcf.com'
    vt_domain_res = search_vt_domain(domain)
    print(vt_domain_res)
if __name__=="__main__":
    main()