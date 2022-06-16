from os import sep
import pandas as pd
from pandas.core.reshape.merge import merge

# Third party libraries
library_path = '/home/budi/crypto_project/crypto_code/static_analysis/report/library_detail_wallet_apps_refined_list.csv'
report_path = '/home/budi/crypto_project/crypto_code/static_analysis/report/'

lib_df = pd.read_csv(library_path)
lib_df = lib_df[['app_id','lib_name']]
# print(lib_df)

lib_write_path = report_path+'app_id_n_lib.txt'
lib_df.to_csv(lib_write_path,sep=';',index=None)

# Third party domain
easylist_path = '/home/budi/crypto_project/crypto_code/dynamic_analysis/easylist.txt'
easypriv_path = '/home/budi/crypto_project/crypto_code/dynamic_analysis/easyprivacy.txt'
fld_path = '/home/budi/crypto_project/crypto_code/dynamic_analysis/report/fld_per_app.csv'

easy_list=[]
with open(easylist_path,'r') as fl:
    for line in fl:
        easy_list.append(line.strip())

with open(easypriv_path,'r') as fl:
    for line in fl:
        easy_list.append(line.strip())

fld_df = pd.read_csv(fld_path)
unique_fld = fld_df['fld']
unique_fld = unique_fld.drop_duplicates().reset_index()
print((unique_fld))

fld_third=[]
for x,line in unique_fld.iterrows():
    print(line)
    for item in easy_list:
        if line['fld'] in item:
            third_item = {'fld':line['fld'],'third_party':'1'}
            fld_third.append(third_item)
            break
third_df = pd.DataFrame(fld_third)
dom_write_path = report_path+'unique_third_dom.txt'
third_df.to_csv(dom_write_path,sep=';',index=None)

