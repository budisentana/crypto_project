import pandas as pd
from pandas.core.reshape.merge import merge 

vt_res_path = '/home/budi/crypto_project/crypto_code/static_analysis/report/vt_sum_per_app_wallet_apps_refined_list.csv'
review_path = '/home/budi/crypto_project/crypto_code/metadata_crawling/sum_negative_review.csv'
metadata_path = '/home/budi/crypto_project/crypto_code/apps_screening/crypto_metadata.csv'

#read metadata
metadata_df = pd.read_csv(metadata_path)
metadata_df = metadata_df[['appId','score','install']]
# print(metadata_df)

#read malware detection
malware_df = pd.read_csv(vt_res_path)
# print(malware_df)

# read the fraudulent category complain
review_df = pd.read_csv(review_path)
negative_df = review_df[['appId','total_negative','total','pct_negative']]
negative_df = negative_df[negative_df['pct_negative']!=0]
# print(fraud_df.sort_values(by=['pct_fraud'],ascending=False))

merge_df = merge(negative_df,malware_df,left_on='appId',right_on='app_id',how='inner')
merge_df=merge_df.drop(columns=['app_id'])
merge_df = merge(merge_df,metadata_df,left_on='appId',right_on='appId',how='inner')
merge_df = merge_df.sort_values(by=['vt_positive'],ascending=False).reset_index()
# print(merge_df.sort_values(by=['vt_positive','pct_negative'],ascending=False))
print(merge_df.sort_values(by=['pct_negative','vt_positive'],ascending=False))

write_path = '/home/budi/crypto_project/crypto_code/static_analysis/report/user_review_vt_score_install.txt'
with open(write_path,'w') as fl:
    for x,line in merge_df.iterrows():
        # fl.write(line['appId']+' & '+str(round(line['pct_negative'],1)))
        fl.write(str(x+1)+' & '+ line['appId']+' & '+str(round(line['pct_negative'],1))+ '\%  &' + str(line['install'])+'+ & '+ str(line['score'])+' & '+
        str(line['vt_positive'])+'\\\ \n' )