import json
import os
import pandas as pd
from vt_work import vt_find_positive

apps_list = '/home/budi/crypto_project/crypto_code/apps_screening/wallet_apps_refined_list.csv'
report_path = '/home/budi/crypto_project/crypto_code/static_analysis/report/'
vt_result_path = '/home/budi/crypto_project/vt_result/'

def check_vt_result(apk_id,vt_path):
    for roots,dirs,files in os.walk(vt_path):
        if apk_id in files:
            return True
        else:
            return False

def main():
    vt_positive_result_list = []
    no_found_list=[]
    with open(apps_list,'r') as app_list:
        for item in app_list:
            item = item.strip('\n')
            check = check_vt_result(item,vt_result_path)
            if check == True:
                vt_result_apk_path = vt_result_path+item
                vt_positive = vt_find_positive(vt_result_apk_path)
                for positive in vt_positive:
                    app_id = {'app_id':item}
                    item_positive = dict(app_id,**positive)
                    vt_positive_result_list.append(item_positive)
            else:
                # print('VT result not found for : '+item)
                no_found_list.append(item)

    """ Summarizing detail virus total positive result"""
    file_sufix = apps_list.split('/')
    file_sufix=file_sufix[-1]
    vt_detail_path = report_path+'vt_positive_detail_'+file_sufix
    for vt in vt_positive_result_list:
        print(vt)
    # write_to_csv(vt_positive_result_list,vt_detail_path)

    """ Summarizing positive virus total per apps"""
    vt_sum_per_app = report_path+'vt_sum_per_app_'+file_sufix
    df_vt = pd.DataFrame(vt_positive_result_list)
    vt_per_app = df_vt.groupby(['app_id'])['app_id'].count().reset_index(name='count')
    print(vt_per_app)
    # write_to_csv(vt_per_app,vt_sum_per_app)


if __name__ == "__main__":
    main()
