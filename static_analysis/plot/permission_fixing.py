import pandas as pd
from pandas.io.parsers import read_csv 
import numpy as np
import statsmodels.api as sm # recommended import according to the docs
import matplotlib.pyplot as plt


permission_detail_path = '/home/budi/crypto_project/crypto_code/static_analysis/report/permission/permission_detail_fixing.csv'
write_path = '/home/budi/crypto_project/crypto_code/static_analysis/plot/'
report_path = '/home/budi/crypto_project/crypto_code/static_analysis/report/'


def not_available_permission(file,write_path):
    percentiles = np.array([25,50 , 85])
    perm = pd.read_csv(file)
    # perm['level'] = perm['level'].str.replace('N/A','unknown')
    perm=perm.fillna('unknown')
    print(perm.head(390))

    cst_perm = perm[perm['level']=='unknown'].groupby(['permission'])['permission'].count().reset_index(name='count').sort_values(by=('count'),ascending=False)
    # print(cst_perm[cst_perm['count']>2])
    print(cst_perm.head(390))


def worth_noting(file,write_path):
    perm = pd.read_csv(file)
    perm=perm.fillna('unknown')

    perm_worth_noting = write_path+'permission_worth_noting.txt'
    df_mount = perm[perm['permission']=='android.permission.MOUNT_UNMOUNT_FILESYSTEMS']
    mount_app_id = df_mount['app_id'].values.tolist()
    mount_perm = df_mount['permission'].values.tolist()
    with open(perm_worth_noting,'w') as ufile:
        ufile.write('----Mount File System Permission--------\n')
        for x,u_item in enumerate(mount_app_id):
            ufile.write(str(mount_app_id[x]).replace('_','\_')+ ' & ' + str(mount_perm[x]).replace('_','\_')+'\\\ \n')
        ufile.write('------------------------------------------------------ \n')

    df_down = perm[perm['permission']=='android.permission.DOWNLOAD_WITHOUT_NOTIFICATION']
    down_app_id = df_down['app_id'].values.tolist()
    down_perm = df_down['permission'].values.tolist()
    with open(perm_worth_noting,'a') as ufile:
        ufile.write('----Download Without Notification Permission--------\n')
        for x,u_item in enumerate(down_app_id):
            ufile.write(str(down_app_id[x]).replace('_','\_')+ ' & ' + str(down_perm[x]).replace('_','\_')+'\\\ \n')
        ufile.write('------------------------------------------------------ \n')

def pct(x):
    n = 457
    res = round((x/n)*100,1)

    return res


def count_per_level(detail_path,report_path):
    perm = pd.read_csv(detail_path)
    perm=perm.fillna('unknown')

    sum_report_path = report_path+'perm_count_per_level.txt'

    unknown_perm = perm[perm['level']=='unknown'].groupby(['permission'])['permission'].count().reset_index(name='count').sort_values(by=('count'),ascending=False)
    perm_name = unknown_perm['permission'].values.tolist()
    perm_count = unknown_perm['count'].values.tolist()
    with open(sum_report_path,'w') as ufile:
        ufile.write('----Unknown Level Permission--------\n')
        ufile.write('Permission_name & count \\\ \n')
        for x,u_item in enumerate(perm_name):
            # print(perm_count[x])
            pct_x = pct(int(perm_count[x]))
            ufile.write(str(perm_name[x]).replace('_','\_')+ ' & ' + str(perm_count[x])+ ' (' + str(pct_x)+'\%)'+'\\\ \n')
        ufile.write('------------------------------------------------------ \n')

    danger_perm = perm[perm['level']=='dangerous'].groupby(['permission'])['permission'].count().reset_index(name='count').sort_values(by=('count'),ascending=False)
    danger_name = danger_perm['permission'].values.tolist()
    danger_count = danger_perm['count'].values.tolist()
    with open(sum_report_path,'a') as ufile:
        ufile.write('----Dangerous Level Permission--------\n')
        ufile.write('Permission_name & count \\\ \n')
        for x,u_item in enumerate(danger_name):
            pct_x = pct(int(danger_count[x]))
            ufile.write(str(danger_name[x]).replace('_','\_')+ ' & ' + str(danger_count[x])+ ' (' + str(pct_x)+'\%)'+'\\\ \n')
        ufile.write('------------------------------------------------------ \n')

    sig_perm = perm[perm['level']=='signature'].groupby(['permission'])['permission'].count().reset_index(name='count').sort_values(by=('count'),ascending=False)
    sig_name = sig_perm['permission'].values.tolist()
    sig_count = sig_perm['count'].values.tolist()
    with open(sum_report_path,'a') as ufile:
        ufile.write('----Signature Level Permission--------\n')
        ufile.write('Permission_name & count \\\ \n')
        for x,u_item in enumerate(sig_name):
            pct_x = pct(int(sig_count[x]))
            ufile.write(str(sig_name[x]).replace('_','\_')+ ' & ' + str(sig_count[x])+ ' (' + str(pct_x)+'\%)'+'\\\ \n')
        ufile.write('------------------------------------------------------ \n')

    norm_perm = perm[perm['level']=='normal'].groupby(['permission'])['permission'].count().reset_index(name='count').sort_values(by=('count'),ascending=False)
    norm_name = norm_perm['permission'].values.tolist()
    norm_count = norm_perm['count'].values.tolist()
    with open(sum_report_path,'a') as ufile:
        ufile.write('----Normal Level Permission--------\n')
        ufile.write('Permission_name & count \\\ \n')
        for x,u_item in enumerate(norm_name):
            pct_x = pct(int(norm_count[x]))
            ufile.write(str(norm_name[x]).replace('_','\_')+ ' & ' + str(norm_count[x])+ ' (' + str(pct_x)+'\%)'+'\\\ \n')
        ufile.write('------------------------------------------------------ \n')

    custom_perm = perm[perm['level']=='customized'].groupby(['permission'])['permission'].count().reset_index(name='count').sort_values(by=('count'),ascending=False)
    custom_name = custom_perm['permission'].values.tolist()
    custom_count = custom_perm['count'].values.tolist()
    with open(sum_report_path,'a') as ufile:
        ufile.write('----Customized Level Permission--------\n')
        ufile.write('Permission_name & count \\\ \n')
        for x,u_item in enumerate(custom_name):
            pct_x = pct(int(custom_count[x]))
            ufile.write(str(custom_name[x]).replace('_','\_')+ ' & ' + str(custom_count[x])+ ' (' + str(pct_x)+'\%)'+'\\\ \n')
        ufile.write('------------------------------------------------------ \n')

def fixing_dict():
    f_dict ={'com.huawei.android.launcher.permission.WRITE_SETTINGS':'customized','com.oppo.launcher.permission.WRITE_SETTINGS':'customized',
    'com.google.android.providers.gsf.permission.WRITE_GSERVICES':'customized'}
    return f_dict

def fixing_detail(detail_path):
    f_dict = fixing_dict()
    # print(f_dict)
    perm = pd.read_csv(detail_path)
    perm=perm.fillna('unknown')
    perm = perm[['app_id','permission','level']]
    for x,item in perm.iterrows():
        str_perm = str(item['permission'])
        if str_perm in f_dict:
            # print(item.values.tolist())    
            item['level'] = f_dict[str_perm]
    perm.to_csv(detail_path)

def count_per_app(detail_path,report_path):
    
    df_perm_detail = pd.read_csv(detail_path)
    df_sum_app = df_perm_detail.groupby(['app_id','level'])['level'].count().unstack().reset_index()
    # print(df_sum_app)
    perm_sum_per_app_path = report_path+'permission_sum_per_app.csv'    
    df_sum_app.to_csv(perm_sum_per_app_path)

    """Summarizing permission per access level"""
    df_sum_total = df_perm_detail.groupby(['level'])['level'].count().reset_index(name='count')
    print(df_sum_total)
    perm_sum_total = report_path+'permission_sum_total.csv'
    df_sum_total.to_csv(perm_sum_total)


def main():
    fixing_detail(permission_detail_path)
    count_per_level(permission_detail_path,report_path)
    count_per_app(permission_detail_path,report_path)
    # fixing_detail(permission_detail_path)
    # cst_plot = write_path+'customized_permission.pdf'
    # not_available_permission(permission_detail_path,cst_plot)

    worth_noting(permission_detail_path,report_path)
    # cst_plot = report_path+'permission_mount_file_system.csv'
    # find_mount_FS(permission_detail_path,cst_plot)

    # cst_plot = report_path+'permission_download_won.csv'
    # find_download_won(permission_detail_path,cst_plot)


if __name__=='__main__':
    main()