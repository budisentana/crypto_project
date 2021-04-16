"""
    This script is used to scrap metatadat per Id
    This script is use to check the paid app
"""

import os
import json
import pandas as pd
import csv

selected_app_id = '/home/budi/adblocker_project/metadata_crawling/add_list.txt'
selected_metadata = '/home/budi/adblocker_project/metadata_crawling/selected_metadata/'
paid_csv = '/home/budi/adblocker_project/metadata_crawling/paid_app.csv'
add_blocker_metadata = '/home/budi/adblocker_project/metadata_crawling/addblocker_metadata.csv'
aps_list=[]
with open(selected_app_id,'r') as app_id:
    for item in app_id:
        item_id = item.strip('\n')
        aps_list.append(item_id)
        # print('Scraping apps metadata Per Id : '+item_id)
        # os.system('node metadata_scraper_per_id.js '+item_id)


"""Read JSON reasult from the scrape result folder"""
paid_app=[]
metadata = []
for item in aps_list:
    app_path = selected_metadata+item+'.txt'
    # print(app_path)
    try:
        with open(app_path,'r') as app_metadata:
            data=app_metadata.read()
            json_data = json.loads(data)
            item_dict = {'appId':json_data['appId'],'install':json_data['installs'],#'score': json_data['score'],
            'genre':json_data['genre'],'price':json_data['price'],
            'currency':json_data['currency'],'free':json_data['free'],'title':json_data['title'],'summary':json_data['summary']}
            metadata.append(item_dict)
            if json_data['free'] == False:
                print(item_dict)
                paid_app.append(item_dict)
    except IOError:
        print(IOError)        


paid_df = pd.DataFrame(paid_app)
metadata_df = pd.DataFrame(metadata)
print(paid_df)
paid_df.to_csv(paid_csv,sep=';')
metadata_df.to_csv(add_blocker_metadata,sep=';')
