import os
import json
import pandas as pd
import csv
import numpy as np
import time
from tld import get_fld,get_tld
from vt_domain_scan import search_vt_domain

netloc_path = '/home/budi/crypto_project/crypto_code/dynamic_analysis/report/netloc_per_app.csv'
domain_report_path = '/home/budi/crypto_project/crypto_code/dynamic_analysis/report/'
vt_domain_result = '/home/budi/crypto_project/vt_domain_result/'

def sum_netloc(netloc_path,report_path):
    netloc_df = pd.read_csv(netloc_path)
    # print(netloc_df)
    netloc_count = netloc_df.groupby(['netloc']).size().reset_index(name='count').sort_values(by=['count'],ascending=False)
    write_path = report_path+'count_netloc.csv'
    netloc_count.to_csv(write_path,index=None)
    # print(netloc_count)
    return netloc_count

def check_result(res_path,domain):
    for roots,dirs,files in os.walk(res_path):
        if domain in files:
            print(domain)
            return True
        else:
            return False

def scan_domain(netloc_df,res_path):
    netloc_list = netloc_df['netloc'].tolist()
    for netloc in netloc_list:
        print('Scan domain : ' + netloc)
        res = check_result(res_path,netloc)
        if res == True:
            print("Netloc scan result available : "+netloc)
        else:
            print("Netloc scan : "+netloc)
            scan_res = search_vt_domain(netloc)
            print(scan_res)
            netloc_res_path = res_path+netloc
            print('write to file :'+netloc_res_path)
            with open (netloc_res_path,'w') as fl:
                json.dump(scan_res,fl)
            time.sleep (16)
def main():
    netloc_df = sum_netloc(netloc_path,domain_report_path)
    scan_domain(netloc_df,vt_domain_result)
    # domain = 'pixel.wp.com'
    # for roots,dirs,files in os.walk(vt_domain_result):
    #     if domain in files:
    #         print(domain)

if __name__=='__main__':
    main()