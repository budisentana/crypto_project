import os
import pandas as pd
from pandas.core.indexes.base import Index
from pandas.io.parsers import read_csv

privacy_res_path = '/home/budi/crypto_project/crypto_code/privacy_policy/report/privacy_policy_refined_test_again_redirect_link.csv'
tracker_res_path = '/home/budi/crypto_project/crypto_code/static_analysis/report/library_detail_wallet_apps_refined_list.csv'
PP_report_path = '/home/budi/crypto_project/crypto_code/privacy_policy/report/'

def check_PP_to_tracker(PP_path,tracker_path,report_path):
    violation_pp_false_dict=[]
    """Read Privacy policy classification result"""
    PP_df = pd.read_csv(PP_path)
    PP_df['Unnamed: 2'] = PP_df['Unnamed: 2'].str.strip()
    PP_df['Unnamed: 3'] = PP_df['Unnamed: 3'].str.strip()
    print(PP_df)
    pp_status = PP_df.groupby(['Unnamed: 2']).size().reset_index(name='count')
    print(pp_status)

    pp_false = PP_df[PP_df['Unnamed: 2']=='False']
    false_path = report_path+'pp_false.csv'
    pp_false.to_csv(false_path)

    pp_false_clean = pp_false[pp_false['Unnamed: 3']=='en']
    false_clean_path = report_path+'pp_false_clean.csv'
    pp_false_clean.to_csv(false_clean_path)
    print(pp_false_clean)

    pp_true = PP_df[PP_df['Unnamed: 2']=='True']
    true_path = report_path+'pp_true.csv'
    pp_true.to_csv(true_path)

    """Read Third party library tracking result"""
    tracker_df = pd.read_csv(tracker_path)

    # print(PP_list)
    pp_false_list = pp_false_clean['Unnamed: 0'].tolist()
    for x,tracker in tracker_df.iterrows():
        app_id = tracker['app_id']
        if app_id in pp_false_list: 
            # print(tracker['app_id'], tracker['lib_name'])
            violation_pp_false_dict.append({'app_id':app_id,'lib_name':tracker['lib_name']})
    df_violator = pd.DataFrame(violation_pp_false_dict)
    print(df_violator)
    detail_report_path = report_path+'violator_detail.csv'
    df_violator.to_csv(detail_report_path)

    df_sum = df_violator.groupby(['app_id']).size().reset_index(name='count')
    sum_report_path = report_path+'violator_sum.csv'
    df_sum.to_csv(sum_report_path)

def pp_sum(pp_path,report_path):
    pp_df = pd.read_csv(pp_path)
    pp_df['Unnamed: 2'] = pp_df['Unnamed: 2'].str.strip() 
    # print(pp_df)
    pp_not_found = pp_df[pp_df['Unnamed: 2']=='None']
    agg_not_found = pp_not_found.groupby(['Unnamed: 4']).size().reset_index(name='count').sort_values(by=['count'],ascending=False)
    print(len(pp_not_found))
    print(agg_not_found)
    write_path = report_path+'failed_to_extract.txt'
    agg_not_found.to_csv(write_path,index=False)

def main():
    check_PP_to_tracker(privacy_res_path,tracker_res_path,PP_report_path)
    # pp_sum(privacy_res_path,PP_report_path)

if __name__=='__main__':
    main()