import sqlite3
from sqlite3 import Error
import pandas as pd
from pandas.core.reshape.merge import merge

db_loc = '/home/budi/crypto_project/crypto_code/dynamic_analysis/vt_scan_report_.db'
netloc_path = '/home/budi/crypto_project/crypto_code/dynamic_analysis/report/netloc_per_app.csv'
write_path = '/home/budi/crypto_project/crypto_code/dynamic_analysis/report/'

def select_data(db_loc,str_query):
    con=sqlite3.connect(db_loc)

    data=pd.read_sql_query(str_query,con)
    return data

def main():
    whitelisted =['www.google.com','www.gstatic.com','graph.facebook.com','connect.facebook.net','firebase-settings.crashlytics.com',
    'www.google-analytics.com','www.googletagmanager.com','stats.g.doubleclick.net','www.google.com.au']
    netloc_df = pd.read_csv(netloc_path)
    netloc_df=netloc_df.drop(columns=['Unnamed: 0'])


    # finding domain with all vt positives
    query1 = "select * from malicious_url_on_domain where npositives>0"
    res1 = select_data(db_loc,query1)
    res1 = res1['domain'].drop_duplicates()   
    netloc_df1 = merge(netloc_df,res1,left_on='netloc',right_on='domain',how='inner')
    netloc_df1 =netloc_df1[~netloc_df1['netloc'].isin(whitelisted)]
    # print(netloc_df1)  
    path_1 = write_path+'netloc_to_malicious_domain_1.csv'
    netloc_df1.to_csv(path_1,index=False)


    query3 = "select * from malicious_url_on_domain where npositives>3"
    res3 = select_data(db_loc,query3)
    res3 = res3['domain'].drop_duplicates()   
    netloc_df3 = merge(netloc_df,res3,left_on='netloc',right_on='domain',how='inner')
    netloc_df3 =netloc_df3[~netloc_df3['netloc'].isin(whitelisted)]
    path_3 = write_path+'netloc_to_malicious_domain_3.csv'
    netloc_df3.to_csv(path_3,index=False)


    query5 = "select * from malicious_url_on_domain where npositives>5"
    res5 = select_data(db_loc,query5)
    res5 = res5['domain'].drop_duplicates()   
    netloc_df5 = merge(netloc_df,res5,left_on='netloc',right_on='domain',how='inner')
    netloc_df5 =netloc_df5[~netloc_df5['netloc'].isin(whitelisted)]
    path_5 = write_path+'netloc_to_malicious_domain_5.csv'
    netloc_df5.to_csv(path_5,index=False)

if __name__=='__main__':
    main()