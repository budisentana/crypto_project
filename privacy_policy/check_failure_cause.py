import os
import pandas as pd
from pandas.core.indexes.base import Index
from pandas.io.parsers import read_csv

failured_source = '/home/budi/crypto_project/crypto_code/privacy_policy/report/failed_to_extract_refined_source.txt'
report_path = '/home/budi/crypto_project/crypto_code/privacy_policy/report/failed_to_extract_refined_result.txt'

def check_failure(source,dest):
    failured_df = pd.read_csv(source,sep='&',index_col=False,header=None)
    # failured_df.columns['error_name','count']
    failured_df[1]=failured_df[1].astype(int)
    with open(dest,'w') as fl:      
        for x,item in failured_df.iterrows():
            pct_x = pct(item[1])
            fl.write(str(x+1)+' & '+item[0]+' & '+ str(item[1])+' ('+str(pct_x)+'\%) \\\ \n')
            print(x+1,item[0],item[1],pct_x)

def pct(x):
    n = 457
    res = round((x/n)*100,1)
    return res

def main():
    check_failure(failured_source,report_path)

if __name__=='__main__':
    main()