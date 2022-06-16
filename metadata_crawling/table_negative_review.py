import pandas as pd

sum_path = '/home/budi/crypto_project/crypto_code/metadata_crawling/sum_negative_review.csv'
detail_path = '/home/budi/crypto_project/crypto_code/apps_screening/comment_file.csv'
write_path = '/home/budi/crypto_project/crypto_code/metadata_crawling/table_content.txt'

def pct(x,y):
    res = round((x/y)*100,1)
    return res


detail_df = pd.read_csv(detail_path,low_memory=False)
detail_df= detail_df[~detail_df['star'].isin(['error'])]
detail_df['star'] = detail_df['star'].astype(int)

negative_length = len(detail_df[detail_df['star']<3])
# print(negative_length)

n = 457 # number of crypto wallet apps
sum_df = pd.read_csv(sum_path)
print(sum_df)

fraud = sum_df[['appId','fraudulent']]
fraud = fraud[fraud['fraudulent']>0]
fraud_sum = fraud['fraudulent'].sum()
pct_sum_fr = pct(fraud_sum,negative_length)
pct_app_fr = pct(len(fraud),n)

bugs = sum_df[['appId','bugs']]
bugs = bugs[bugs['bugs']>0]
bugs_sum = bugs['bugs'].sum()
pct_sum_bg = pct(bugs_sum,negative_length)
pct_app_bg = pct(len(bugs),n)

auth = sum_df[['appId','authentication']]
auth = auth[auth['authentication']>0]
auth_sum = auth['authentication'].sum()
pct_sum_au = pct(auth_sum,negative_length)
pct_app_au = pct(len(auth),n)

sec = sum_df[['appId','security']]
sec = sec[sec['security']>0]
sec_sum = sec['security'].sum()
pct_sum_se = pct(sec_sum,negative_length)
pct_app_se = pct(len(sec),n)

usa = sum_df[['appId','usability']]
usa = usa[usa['usability']>0]
usa_sum = usa['usability'].sum()
pct_sum_us = pct(usa_sum,negative_length)
pct_app_us = pct(len(usa),n)

ads = sum_df[['appId','ads_tracker']]
ads = ads[ads['ads_tracker']>0]
ads_sum = ads['ads_tracker'].sum()
pct_sum_ad = pct(ads_sum,negative_length)
pct_app_ad = pct(len(ads),n)

with open(write_path,'w') as fl:
    fl.write('Fraudulent'+' & '+str(fraud_sum)+' ('+str(pct_sum_fr)+'\%)'+' & '+str(len(fraud))+' ('+str(pct_app_fr)+'\%) & \n')
    fl.write('Bugs'+' & '+str(bugs_sum)+' ('+str(pct_sum_bg)+'\%)'+' & '+str(len(bugs))+' ('+str(pct_app_bg)+'\%) & \n')   
    fl.write('Authentication'+' & '+str(auth_sum)+' ('+str(pct_sum_au)+'\%)'+' & '+str(len(auth))+' ('+str(pct_app_au)+'\%) & \n') 
    fl.write('Security'+' & '+str(sec_sum)+' ('+str(pct_sum_se)+'\%)'+' & '+str(len(sec))+' ('+str(pct_app_se)+'\%) & \n')
    fl.write('Usability'+' & '+str(usa_sum)+' ('+str(pct_sum_us)+'\%)'+' & '+str(len(usa))+' ('+str(pct_app_us)+'\%) & \n')
    fl.write('Ads and Tracker'+' & '+str(ads_sum)+' ('+str(pct_sum_ad)+'\%)'+' & '+str(len(ads))+' ('+str(pct_app_ad)+'\%) & \n')