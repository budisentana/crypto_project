import os

playstore_url = 'market://details?id='
app_list_path ='/home/budi/crypto_project/crypto_code/apps_download/new_apk_list.txt'
racoon_list_path = '/home/budi/crypto_project/crypto_code/apps_download/racoon_list.txt'


def extract_list(app_list_path,playstore_url):
    app_url=[]
    with open (app_list_path,'r') as fl:
        for line in fl:
            line_id = playstore_url+line.strip('\n')
            app_url.append(line_id)

    return app_url

def write_to_file(racoon_list,write_path):
    with open(write_path,'w')as fl:
        for item in racoon_list:
            fl.write(item+'\n')
def main():
    res = extract_list(app_list_path,playstore_url)
    write_to_file(res,racoon_list_path)
    for item in res:
        print(item)

if __name__=='__main__':
    main()