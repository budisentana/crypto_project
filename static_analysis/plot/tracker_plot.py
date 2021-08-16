import pandas as pd
from pandas.io.parsers import read_csv 
import numpy as np
import statsmodels.api as sm # recommended import according to the docs
import matplotlib.pyplot as plt


tracker_path = '/home/budi/crypto_project/crypto_code/static_analysis/report/library_detail_wallet_apps_refined_list.csv'
write_path = '/home/budi/crypto_project/crypto_code/static_analysis/plot/'


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


def main():
    ecdf_path = write_path+'tracker_ecdf.pdf'
    tracker_ecdf(tracker_path,ecdf_path)

    bar_path = write_path+'tracker_bar.pdf'
    tracker_bar(tracker_path,bar_path)


if __name__=='__main__':
    main()