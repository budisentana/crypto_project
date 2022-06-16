from os import sep
import pandas as pd
from pandas.core.reshape.merge import merge 

fld_path = '/home/budi/crypto_project/crypto_code/dynamic_analysis/report/fld_per_app.csv'
third_party_domain_path = '/home/budi/crypto_project/crypto_code/static_analysis/report/unique_third_dom.txt'
report_path = '/home/budi/crypto_project/crypto_code/dynamic_analysis/report/'

fld_df = pd.read_csv(fld_path)
print(fld_df)

third_df = pd.read_csv(third_party_domain_path,sep=';')
print(third_df)

fld_df = merge(fld_df,third_df,left_on='fld',right_on='fld',how='left')
fld_df.dropna(subset = ["third_party"], inplace=True)
fld_df = fld_df[['app_id','fld']]
third_party_path = report_path+'appId_n_third_party_domain.txt'
fld_df.to_csv(third_party_path,sep=';',index=False)
print(fld_df)