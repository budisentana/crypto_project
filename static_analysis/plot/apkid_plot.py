from operator import index
import pandas as pd
from pandas.core.algorithms import value_counts
from pandas.io.parsers import read_csv 
import numpy as np
import statsmodels.api as sm # recommended import according to the docs
import matplotlib.pyplot as plt


apkid_path = '/home/budi/crypto_project/crypto_code/static_analysis/report/apkid_sum_wallet_apps_refined_list.csv'
write_path = '/home/budi/crypto_project/crypto_code/static_analysis/plot/'
apkid_raw_path = '/home/budi/crypto_project/crypto_code/static_analysis/report/apkid_detail_wallet_apps_refined_list.csv'

def apkid_plot(file,plot_path):
    df_apkid = pd.read_csv(file)
    sum_df_apkid= df_apkid[['anti_vm','obfuscator','anti_debug','anti_disassembly','manipulator','packer']].sum().reset_index(name='count')
    sum_df_apkid = sum_df_apkid.sort_values(by=['count'])#,ascending=False)
    print(sum_df_apkid)

    parameter = sum_df_apkid['index']
    count = sum_df_apkid['count']
    fig = plt.figure(figsize=(6,4))
    plt.xticks(rotation='vertical',fontsize=12)
    plt.barh(parameter, count)
    plt.ylabel('Parameter',fontsize=12)
    plt.xlabel('# of Apps',fontsize=12)
    plt.tight_layout()
    fig.savefig(plot_path)
    plt.show()

def dexer_plot(file,write_path):
    compiler_list =[]
    dexer_data = pd.read_csv(file)
    # print(dexer_data)
    for index,line in dexer_data.iterrows():
        # print(line['app_name'])
        if line['types'] == 'compiler' :
            if 'r8' in line['matches']:
                compiler = 'R8' 
            elif 'unknown' in  line['matches']:
                compiler = 'unknown'
            elif 'dexmerge' in line['matches']:
                compiler = 'dexmerge'
            elif 'dexlib' in line['matches']:
                compiler = 'dexlib'
            else:
                compiler = 'dx'

            comp_item = {'app_id':line['app_name'],'compiler':compiler}
            if comp_item not in compiler_list:
                compiler_list.append(comp_item)
    df_comp = pd.DataFrame(compiler_list)
    df_comp_type = df_comp.groupby(['compiler']).size().reset_index(name='count')
    print(df_comp_type)
    # print(df_comp_type['compiler'],df_comp_type['count'])
    pie_val = df_comp_type['count']
    labels = df_comp_type['compiler']
    fig = plt.figure(figsize=(6,4))
    plt.pie(pie_val,labels=labels, autopct='%.0f%%', textprops={'color':"w"})
    # plt.title("Dex File Compiler Type")
    plt.legend()
    fig.savefig(write_path)
    plt.show()

def main():
    plot_path = write_path+'anti_analysis_plot.pdf'
    # apkid_plot(apkid_path,plot_path)
    compiler_plot_path = write_path+'compiler_type_plot.pdf'
    dexer_plot(apkid_raw_path,compiler_plot_path)

if __name__=='__main__':
    main()