"""
    This script is used to scrap metatadat per Id
"""

import os
import json
import pandas as pd
import csv

node_js_path = '/home/budi/crypto_project/crypto_code/apps_screening/'
selected_app_id = '/home/budi/crypto_project/crypto_code/apps_screening/all_downloaded_310_appIDs.csv'
selected_metadata = '/home/budi/crypto_project/crypto_code/apps_screening/selected_metadata/'
crypto_metadata_file = '/home/budi/crypto_project/crypto_code/apps_screening/crypto_metadata.csv'
apps_not_found = '/home/budi/crypto_project/crypto_code/apps_screening/app_not_found.csv'

def scrap_metadata_js (app_id, nodejs_path,result_path):
    print('Change directory to node js')
    current_dir = os.getcwd()
    os.chdir(node_js_path)
    print('Scraping apps metadata Per Id : '+app_id)
    os.system('node metadata_scraper_per_id.js '+app_id+' '+result_path)
    os.chdir(current_dir)

def encode_metadata(app_id,res_path):
    """Read JSON reasult from the scrape result folder"""
    app_id_res = res_path+app_id+'.txt'
    print(app_id_res)
    item_dict=[]
    try:
        with open(app_id_res,'r') as app_metadata:
            data=app_metadata.read()
            # print(data)
            json_data = json.loads(data)
            app_id = json_data['appId'] if 'appId' in json_data else None
            app_title = json_data['title']
            score = json_data['scoreText'] if 'scoreText' in json_data else None
            rating =  json_data['ratings']if 'ratings' in json_data else None
            review = json_data['reviews'] if 'reviews' in json_data else None
            comment = json_data['comments'] if 'comments' in json_data else None

            item_dict = {'appId':app_id, 'title':app_title,
            'score': score,'rating': rating,'review': review,#}
            'comment':comment}
            # print(item_dict)

            # item_dict = {'appId':json_data['appId'],'install':json_data['installs'],'score': json_data['score'],
            # 'genre':json_data['genre'],'price':json_data['price'],
            # 'currency':json_data['currency'],'free':json_data['free'],'title':json_data['title'],'summary':json_data['summary']}
            # print(item_dict)
    except IOError:
        item_dict={'appId':app_id,'title':'error',
            'score': 'error','rating': 'error','review': 'error',#}
            'comment':'error'}        
    return item_dict

# paid_df = pd.DataFrame(paid_app)
# metadata_df = pd.DataFrame(metadata)
# print(paid_df)
# paid_df.to_csv(paid_csv,sep=';')
# metadata_df.to_csv(add_blocker_metadata,sep=';')


def main():
    aps_list=[]
    error_list = []
    with open(selected_app_id,'r') as app_id:
        for item in app_id:           
            item_id = item.strip('\n')
            print(item_id)
            # scrap_metadata_js(item_id,node_js_path,selected_metadata)
            res_metadata=encode_metadata(item_id,selected_metadata)
            # print(res_metadata)
            aps_list.append(res_metadata)
            if res_metadata['title'] == 'error':
                error_list.append(res_metadata)
            # res_metadata=encode_metadata('com.bixin.bixin_android',selected_metadata)
            # print(res_metadata)

    metadata_df = pd.DataFrame(aps_list)
    print(metadata_df)
    metadata_df.to_csv(crypto_metadata_file)

    error_df = pd.DataFrame(error_list)
    print(error_df)
    error_df.to_csv(apps_not_found)

if __name__ == "__main__":
    main()
