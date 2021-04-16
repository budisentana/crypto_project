import os
import pandas as pd
import csv

scrap_path = '/home/budi/crypto_project/crypto_code/apps_screening/crypto_metadata.csv'
apk_list = '/home/budi/crypto_project/crypto_code/apps_download/apk_list.txt'

pd_data = pd.read_csv(scrap_path,sep=';',usecols=['appId'])
print(pd_data)

pd_data.to_csv(apk_list,header=None, index=None)