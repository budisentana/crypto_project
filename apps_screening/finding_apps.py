"""
   Crawling apps metadata containing a certain keywords
   parsing parameter to metadata_scraper.js
"""

import time 
import os
import json
import pandas as pd
import csv

# res_path = '/home/budi/crypto_project/crypto_code/apps_screening/res_by_keyword_exchange/'
# csv_path = '/home/budi/crypto_project/crypto_code/apps_screening/exchange_metadata.csv'
# res_path = '/home/budi/crypto_project/crypto_code/apps_screening/res_by_keyword/'
# csv_path = '/home/budi/crypto_project/crypto_code/apps_screening/crypto_metadata.csv'
# keyword = ["'crypto wallet'","'bitcoin wallet'","'cryptocurrency'","'cryptocurrency wallet'"]
# keyword = ['ethereum', 'litecoin', 'cardano', 'polkadot', 'bitcoin cash', 'stellar', 'chainlink', "'binance coin'", 'tether',\
#  'monero','ETH','LTC','ADA','DOT','BCH','XLM','BNB','USDT','XMR']
# keyword = ['"cryptocurrency exchange"','"crypto exchange"','"ethereum exchange"', '"litecoin exchange"', '"cardano exchange"', \
    # '"polkadot exchange"', '"bitcoin cash exchange"', '" exchange"', '"chainlink exchange"', "'binance coin exchange'", '"tether exchange"',\
    # '"monero exchange"','"ETH exchange"','"LTC exchange"','"ADA coin exchange"','"DOT exchange"','"BCH exchange"','"XLM exchange"','"BNB exchange"',
    # '"USDT exchange"','"XMR exchange"']

npm_path = '/home/budi/crypto_project/crypto_code/apps_screening/'
res_path = '/home/budi/crypto_project/crypto_code/apps_screening/res_merge_all_keyword/'
csv_path = '/home/budi/crypto_project/crypto_code/apps_screening/merge_keyword_metadata.csv'
keyword = ["'crypto wallet'","'bitcoin wallet'","'cryptocurrency'","'cryptocurrency wallet'", 'ethereum', 'litecoin', 'cardano', 'polkadot', "'bitcoin cash'", \
    'stellar', 'chainlink', "'binance coin'", 'tether',"'best crypto wallet'",\
    'monero','ETH','LTC','ADA','DOT','BCH','XLM','BNB','USDT','XMR',\
    'crypto', 'coin', 'bitcoin']

def scrap_by_keyword(result_path,npm_path,keyword):
    print ('Scrapping Apps Metadata using keyword :'+keyword)
    # file_path = result_path+keyword
    os.chdir(npm_path)
    os.system('node metadata_scraper '+keyword+' '+result_path)

def check_existing_result(result_path,keyword_list):
    existing_list = []
    new_list=[]
    for roots,dirs,files in os.walk(result_path):
        for file in files:
            check_file = (file.strip('.txt'))
            existing_list.append(check_file)
    for item in keyword_list:
        if item not in existing_list:
            new_list.append(item)
    return new_list

def encode_metadata(keyword,res_path):
    """Read JSON reasult from the scrape result folder"""
    keyword = keyword.strip("'")
    keyword_res = res_path+keyword+'.txt'
    item_dict=[]
    try:
        with open(keyword_res,'r') as app_metadata:
            data=app_metadata.read()
            json_data = json.loads(data)
            for item in json_data:
                app_id = item['appId'] if 'appId' in item else None
                app_title = item['title'] if 'title' in item else None
                genre = item['genreId'] if 'genreId' in item else None
                # description = item['description'] if 'description' in item else None

                item_dict.append({'appId':app_id, 'title':app_title,'genre':genre})
                # item_dict.append({'appId':app_id, 'title':app_title,'description':description.strip('\n')})

    except IOError:
        print(IOError)
    return item_dict


def main():
    metadata_list=[]
    new_list = check_existing_result(res_path,keyword)
    for item in new_list:
        scrap_by_keyword(res_path,npm_path,item)
        time.sleep(3)

        meta_res = encode_metadata(item,res_path)
        for item in meta_res:
            if item not in metadata_list:
                metadata_list.append(item)

    metadata_df = pd.DataFrame(metadata_list)
    print(metadata_df)
    metadata_df.to_csv(csv_path)


if __name__=='__main__':
    main()
