import os
import json
import pandas as pd
import csv
import numpy as np
from tld import get_fld,get_tld

# app_list_path ='/home/budi/crypto_project/crypto_code/static_analysis/test.csv'
app_list_path = '/home/budi/crypto_project/crypto_code/apps_screening/wallet_apps_refined_list.csv'
har_dir_path = '/home/budi/crypto_project/har_file/'
domain_report_path = '/home/budi/crypto_project/crypto_code/dynamic_analysis/report/'

def find_traffic_on_har (har_file_path):
    fld_list=[]
    netloc_list=[]
    with open (har_file_path) as rsf:
        data = rsf.read()
        json_data = json.loads(data)
        json_log = json_data['log']
        for item in json_log:
            json_item = json_log['entries']
            for sub_item in json_item:
                url_ori = sub_item['request']['url']
                try:
                    res_tld = get_tld(url_ori,as_object=True)
                    # fld_item = {'app_id':file,'first_level_domain':res_tld.fld}
                    # netloc_item = {'app_id':file,'first_level_domain':res_tld.parsed_url.netloc}
                    fld_item = res_tld.fld
                    netloc_item = res_tld.parsed_url.netloc

                    if fld_item not in fld_list:
                        fld_list.append(fld_item)
                    if netloc_item not in netloc_list:
                        netloc_list.append(netloc_item)
                except:
                    pass
    return fld_list,netloc_list



def write_traffic_to_file(file_name,new_dir,fld,netloc):
    fld_list=[]
    netloc_list=[]
    write_fld = new_dir+'/'+file_name+'_fld.csv'
    write_netloc =  new_dir+'/'+file_name+'_netloc.csv'
    print(write_netloc)
    for item in fld:
        fld_list.append({'app_id':file_name,'first_level_domain':item})
    
    for item in netloc:
        netloc_list.append({'app_id':file_name,'netloc':item})
    
    df_fld = pd.DataFrame(fld_list)           
    df_fld.to_csv(write_fld)

    df_netloc = pd.DataFrame(netloc_list)           
    df_netloc.to_csv(write_netloc)
 

def listing_app(app_path):
    app_list=[]
    with open(app_path,'r') as fl:
        for item in fl:
            app_list.append(item.strip())
            # print(item)
    return app_list

def check_har_file(har_path,har_file):
    for roots,dirs,files in os.walk(har_path):
        har_check = har_file+'.har'
        if har_check in files:
            return True
        else:
            return False

def main():
    app_list = listing_app(app_list_path)
    no_har_list =[]
    # print(app_list)
    netloc_data =[]
    fld_data =[]
    for app in app_list:
        res = check_har_file(har_dir_path,app)
        if res == True:
            har_file_path = har_dir_path+app+'.har'
            fld_list,netloc_list = find_traffic_on_har(har_file_path)
            for netloc in netloc_list:
                netloc_item = {'app_id':app,'netloc':netloc}
                if netloc_item not in netloc_data:
                    netloc_data.append(netloc_item)            
        
            for fld in fld_list:
                fld_item = {'app_id':app,'fld':fld}
                if fld_item not in fld_data:
                    fld_data.append(fld_item) 
        else:
            no_har_list.append(app)
            print('No har file')

    netloc_df = pd.DataFrame(netloc_data)
    write_netloc_path = domain_report_path+'netloc_per_app.csv'
    netloc_df.to_csv(write_netloc_path)
    print(netloc_df)

    fld_df = pd.DataFrame(fld_data)
    write_fld_path = domain_report_path+'fld_per_app.csv'
    fld_df.to_csv(write_fld_path)

    no_har_df = pd.DataFrame(no_har_list)
    write_no_har_path = domain_report_path+'no_har_app.csv'
    no_har_df.to_csv(write_no_har_path)

if __name__=='__main__':
    main()