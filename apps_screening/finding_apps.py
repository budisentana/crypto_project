"""
   Crawling apps metadata containing a certain keywords
   parsing parameter to metadata_scraper.js
"""

import os
import json
import pandas as pd
import csv

res_path = '/home/budi/crypto_project/crypto_code/apps_screening/res_by_keyword/'
csv_path = '/home/budi/crypto_project/crypto_code/apps_screening/crypto_metadata.csv'
keyword = ["'crypto wallet'","'bitcoin wallet'","'cryptocurrency'","'cryptocurrency wallet'"]

# for item in keyword:
#     print('Scraping apps metadata using keyword : '+item)
#     os.system('node metadata_scraper '+item+' '+res_path)

"""Read JSON reasult from the scraper"""
ad_dict=[]
for root, dirs, files in os.walk(res_path):
    for file in files:
        with open(res_path+file) as source_file:
            data= source_file.read()
            json_data = json.loads(data)
            for item in json_data:
                print(item['appId'])
                item_dict = {'appId':item['appId'],'title':item['title'],'summary':item['summary']}
                if item_dict not in ad_dict:
                    ad_dict.append(item_dict)

# pd_res = pd.DataFrame(ad_dict)
for item in ad_dict:
    print(item['appId'],item['summary'])

csv_columns = ['appId','title','summary']
try:
    with open(csv_path, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns,delimiter=';')
        writer.writeheader()
        for data in ad_dict:
            writer.writerow(data)
except IOError:
    print("I/O error")