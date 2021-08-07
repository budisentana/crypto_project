from operator import index
import pandas as pd
from pandas.core.algorithms import value_counts
from pandas.io.parsers import read_csv 
import numpy as np
import statsmodels.api as sm # recommended import according to the docs
import matplotlib.pyplot as plt


apkid_path = '/home/budi/crypto_project/crypto_code/static_analysis/report/apkid_sum_wallet_apps_refined_list.csv'
write_path = '/home/budi/crypto_project/crypto_code/static_analysis/plot/'

def apkid_plot(file):
    df_apkid = pd.read_csv(file)
    # print(df_apkid)
    # sum_df_apkid = df_apkid.groupby(['anti_vm','obfuscator'])['anti_vm','obfuscator'].size().reset_index()
    sum_df_apkid= df_apkid[['anti_vm','obfuscator','anti_debug','anti_disassembly','manipulator','packer']].sum().reset_index(name='count')
    sum_df_apkid = sum_df_apkid.sort_values(by=['count'])#,ascending=False)
    print(sum_df_apkid)

    parameter = sum_df_apkid['index']
    count = sum_df_apkid['count']
    fig = plt.figure(figsize=(6,4))
    plt.xticks(rotation='vertical')
    plt.barh(parameter, count)
    plt.ylabel('Parameter')
    plt.xlabel('# of Apps')
    plt.tight_layout()
    plt.show()

def sum_negative_review(file,write_path):
    negative_review = read_csv(file)
    hit = negative_review[['fraudulent','bugs','authentication','security','usability','ads_tracker','cust_support']]
    sum_hit = hit.sum(axis=0)
    pct_hit = negative_review[['pct_fraud','pct_bugs','pct_auth','pct_sec','pct_usa','pct_ads','pct_cust']]
    avg_pct = round(pct_hit.mean(axis=0),2)
    result = pd.concat([sum_hit,avg_pct],axis=0)
    print(result)    
    result.to_csv(write_path)


def plot_by_range(file):
    df = pd.read_csv(file)
    df_half = df[['fraudulent','bugs','authentication','security','usability','ads_tracker','cust_support']]
    # print(df_half)
    # range = [0, 25, 50, 75, 100, 125, 150, 175, 200]
    # count_fraud = df_half['fraudulent'].value_counts(bins=range, sort=False)
    # count_fraud.plot(kind='hist')
    count_fraud = pd.cut(df_half['cust_support'],bins=10).value_counts() 
    print(count_fraud) 


 
def main():
    apkid_plot(apkid_path)

if __name__=='__main__':
    main()