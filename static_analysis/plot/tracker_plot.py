from operator import concat
import pandas as pd
from pandas.io.parsers import read_csv 
import numpy as np
import statsmodels.api as sm # recommended import according to the docs
import matplotlib.pyplot as plt


tracker_path = '/home/budi/crypto_project/crypto_code/static_analysis/report/library_detail_wallet_apps_refined_list.csv'
write_path = '/home/budi/crypto_project/crypto_code/static_analysis/plot/'
selected_app_id = '/home/budi/crypto_project/crypto_code/apps_screening/wallet_apps_refined_list.csv'
report_path='/home/budi/crypto_project/crypto_code/static_analysis/report/'


def tracker_ecdf(file,write_path):
    percentiles = np.array([25,50 , 85])
    tracker = pd.read_csv(file)
    tracker=tracker.fillna(0)
    # print(tracker)

    df_third = tracker.groupby(['app_id'])['app_id'].count().reset_index(name='all_lib').sort_values(by=['all_lib'],ascending=False)
    # print(df_tracker)

    df_ads = tracker[tracker['TargetedAds']==True].groupby(['app_id'])['app_id'].count().reset_index(name='ads').sort_values(by=['ads'],ascending=False)
    print(df_ads)

    df_tracker = pd.merge(df_third,df_ads,on='app_id')
    print(df_tracker)

    third = df_tracker['all_lib']
    third_ecdf = sm.distributions.ECDF(third) 
    third_x = np.linspace(min(third), max(third))
    third_y = third_ecdf(third_x)
    third_val = np.percentile(third, percentiles)

    ads = df_tracker['ads']
    ads_ecdf = sm.distributions.ECDF(ads) 
    ads_x = np.linspace(min(ads), max(ads))
    ads_y = ads_ecdf(ads_x)
    ads_val = np.percentile(ads, percentiles)

    fig = plt.figure(figsize=(5,4))
    plt.plot(third_x, third_y*100, linestyle='--', lw = 2)
    plt.plot(ads_x, ads_y*100, linestyle='--', lw = 2)
    plt.legend(("All Libraries", "Ads & Tracker"))
    plt.xlabel('# of Libraries', size = 10)
    plt.ylabel('ECDF', size = 10)
    plt.plot(third_val, percentiles, marker='o', color='red',linestyle='none')
    plt.plot(ads_val, percentiles, marker='o', color='red',linestyle='none')
    fig.savefig(write_path)
    plt.show()

def tracker_bar(file,write_path):
    tracker = pd.read_csv(file)
    tracker=tracker.fillna(0)

    df_ads = tracker[tracker['TargetedAds']==True].groupby(['lib_name'])['lib_name'].count().reset_index(name='count').sort_values(by=['count'],ascending=False)
    print(df_ads.head(20))    

    parameter = df_ads['lib_name'].head(20)
    count = df_ads['count'].head(20)
    fig = plt.figure(figsize=(5,4))
    plt.xticks(rotation='vertical',fontsize=12)
    plt.bar(parameter, count)
    plt.ylabel('# of Apps',fontsize=12)
    plt.xlabel('Ads and Tracker Libraries',fontsize=12)
    plt.tight_layout()
    fig.savefig(write_path)
    plt.show()

def ecdf_third(file,app_list_path,write_path):
    lib_df = pd.read_csv(file)
    lib_df['lib_type'] = lib_df['lib_type'].replace('Utilities','Utility')
    lib_df['lib_type'] = lib_df['lib_type'].replace('Mobile analytics','Analytics')
    lib_df = lib_df[['app_id','lib_name','lib_type']]

    lib_df_app = lib_df.groupby(['app_id','lib_type']).size().unstack().reset_index()
    lib_df_app = lib_df_app[['app_id','Analytics','Payment','Social networking service','Targeted ads']]
    # print(lib_df_app)

    app_list = pd.read_csv(app_list_path,names=['app_id'],header=None)
    # print(app_list)
    merge_df = pd.merge(app_list,lib_df_app,left_on='app_id',right_on='app_id',how='left')
    merge_df = merge_df.fillna(0)
    print(merge_df)

    percentiles = np.array([25,50 , 85])
    anal = merge_df['Analytics']
    anal_ecdf = sm.distributions.ECDF(anal) 
    anal_x = np.linspace(min(anal), max(anal))
    anal_y = anal_ecdf(anal_x)
    anal_val = np.percentile(anal, percentiles)

    pay = merge_df['Payment']
    pay_ecdf = sm.distributions.ECDF(pay) 
    pay_x = np.linspace(min(pay), max(pay))
    pay_y = pay_ecdf(pay_x)
    pay_val = np.percentile(pay, percentiles)

    soc = merge_df['Social networking service']
    soc_ecdf = sm.distributions.ECDF(soc) 
    soc_x = np.linspace(min(soc), max(soc))
    soc_y = soc_ecdf(soc_x)
    soc_val = np.percentile(soc, percentiles)

    ads = merge_df['Targeted ads']
    ads_ecdf = sm.distributions.ECDF(ads) 
    ads_x = np.linspace(min(ads), max(ads))
    ads_y = ads_ecdf(ads_x)
    ads_val = np.percentile(ads, percentiles)

    fig = plt.figure(figsize=(5,4))
    plt.plot(anal_x, anal_y*100, linestyle='--', lw = 2)
    plt.plot(pay_x, pay_y*100, linestyle='--', lw = 2)
    plt.plot(soc_x, soc_y*100, linestyle='--', lw = 2)
    plt.plot(ads_x, ads_y*100, linestyle='--', lw = 2)
    plt.legend(("Analytics", "Payment", "Social media","Ads & Tracker"))
    plt.xlabel('# of Libraries', size = 10)
    plt.ylabel('ECDF', size = 10)
    # plt.plot(anal_val, percentiles, marker='o', color='red',linestyle='none')
    # plt.plot(pay_val, percentiles, marker='o', color='red',linestyle='none')
    # plt.plot(soc_val, percentiles, marker='o', color='red',linestyle='none')
    # plt.plot(ads_val, percentiles, marker='o', color='red',linestyle='none')
    fig.savefig(write_path)
    plt.show()

def sum_dominant_lib(file,write_path):
    lib_df = pd.read_csv(file)
    lib_df['lib_type'] = lib_df['lib_type'].replace('Utilities','Utility')
    lib_df['lib_type'] = lib_df['lib_type'].replace('Mobile analytics','Analytics')
    lib_df = lib_df[['app_id','lib_name','lib_type']]
    # print(lib_df)
    anal_sum = lib_df[lib_df['lib_type']=='Analytics'].groupby(['lib_name']).size().reset_index(name='count').sort_values(by=['count'],ascending=False)
    pay_sum = lib_df[lib_df['lib_type']=='Payment'].groupby(['lib_name']).size().reset_index(name='count').sort_values(by=['count'],ascending=False)
    soc_sum = lib_df[lib_df['lib_type']=='Social networking service'].groupby(['lib_name']).size().reset_index(name='count').sort_values(by=['count'],ascending=False)
    ads_sum = lib_df[lib_df['lib_type']=='Targeted ads'].groupby(['lib_name']).size().reset_index(name='count').sort_values(by=['count'],ascending=False)

    with open(write_path,'w') as fl:
        fl.write('Analytics Libraries\n')
        fl.write('----------------------------\n')
        for x,item in anal_sum.iterrows():
            fl.write(str(item['lib_name'])+' & '+str(item['count'])+'\\\ \n')    
        fl.write('----------------------------\n')

        fl.write('Payment Libraries\n')
        fl.write('----------------------------\n')
        for x,item in pay_sum.iterrows():
            fl.write(str(item['lib_name'])+' & '+str(item['count'])+'\\\ \n')    
        fl.write('----------------------------\n')

        fl.write('Social Media Libraries\n')
        fl.write('----------------------------\n')
        for x,item in soc_sum.iterrows():
            fl.write(str(item['lib_name'])+' & '+str(item['count'])+'\\\ \n')    
        fl.write('----------------------------\n')

        fl.write('Ads and Tracker Libraries\n')
        fl.write('----------------------------\n')
        for x,item in ads_sum.iterrows():
            fl.write(str(item['lib_name'])+' & '+str(item['count'])+'\\\ \n')    
        fl.write('----------------------------\n')

def main():
    # ecdf_path = write_path+'tracker_ecdf.pdf'
    # tracker_ecdf(tracker_path,ecdf_path)

    # bar_path = write_path+'tracker_bar.pdf'
    # tracker_bar(tracker_path,bar_path)

    third_path = write_path+'lib_third_ecdf.pdf'
    ecdf_third(tracker_path,selected_app_id ,third_path)

    dominant_path = report_path+'lib_dominant.txt'
    sum_dominant_lib(tracker_path,dominant_path)

if __name__=='__main__':
    main()