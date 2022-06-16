import pandas as pd
from pandas.io.parsers import read_csv 
import numpy as np
import statsmodels.api as sm # recommended import according to the docs
import matplotlib.pyplot as plt


permission_sum_per_app_path = '/home/budi/crypto_project/crypto_code/static_analysis/report/permission/permission_sum_per_app.csv'
permission_detail_path = '/home/budi/crypto_project/crypto_code/static_analysis/report/permission_detail_wallet_apps_refined_list.csv'
write_path = '/home/budi/crypto_project/crypto_code/static_analysis/plot/'

def permission_plot(file,write_path):
    percentiles = np.array([25,50 , 85])
    perm = pd.read_csv(file)
    perm=perm.fillna(0)
    print(perm)

    dangerous = perm['dangerous']
    dgr_ecdf = sm.distributions.ECDF(dangerous) 
    dgr_x = np.linspace(min(dangerous), max(dangerous))
    print(dgr_x)
    dgr_y = dgr_ecdf(dgr_x)
    dgr_val = np.percentile(dangerous, percentiles)

    normal = perm['normal']
    nrm_ecdf = sm.distributions.ECDF(normal) 
    nrm_x = np.linspace(min(normal), max(normal))
    nrm_y = nrm_ecdf(nrm_x)
    nrm_val = np.percentile(normal, percentiles)

    signature = perm['signature']
    sgt_ecdf = sm.distributions.ECDF(signature) 
    sgt_x = np.linspace(min(signature), max(signature))
    sgt_y = sgt_ecdf(sgt_x)
    sgt_val = np.percentile(signature, percentiles)

    customized = perm['customized']
    cst_ecdf = sm.distributions.ECDF(customized) 
    cst_x = np.linspace(min(customized), max(customized))
    cst_y = cst_ecdf(cst_x)
    cst_val = np.percentile(customized, percentiles)

    fig = plt.figure(figsize=(5,4))
    # plt.plot(dgr_x, dgr_y*100, linestyle='--', lw = 2, color='red')
    # plt.plot(nrm_x, nrm_y*100, linestyle='--', lw = 2, color='green')
    # plt.plot(sgt_x, sgt_y*100, linestyle='--', lw = 2, color='blue')
    # plt.plot(cst_x, cst_y*100, linestyle='--', lw = 2, color='orange')
    plt.plot(dgr_x, dgr_y*100, marker='o', lw = 2, color='red')
    plt.plot(nrm_x, nrm_y*100, marker='^', lw = 2, color='green')
    plt.plot(sgt_x, sgt_y*100, marker='s', lw = 2, color='blue')
    plt.plot(cst_x, cst_y*100, marker='X', lw = 2, color='orange')
    plt.xlim(0,max(cst_x))
    plt.ylim(0,max(cst_y)*100)
    plt.legend(("Dangerous", "Normal","Signature","Customized"))
    # plt.rc('axes', labelsize=18)
    # plt.rc('legend', fontsize=18) 
    plt.xlabel('# of Permission', size = 14)
    plt.ylabel('ECDF', size = 14)
    plt.tight_layout()
    # plt.plot(dgr_val, percentiles, marker='o', color='red',linestyle='none')
    # plt.plot(nrm_val, percentiles, marker='o', color='red',linestyle='none')
    # plt.plot(sgt_val, percentiles, marker='o', color='red',linestyle='none')
    # plt.plot(cst_val, percentiles, marker='o', color='red',linestyle='none')
    fig.savefig(write_path)
    plt.show()

def percentage_plot(file,write_path):
    percentiles = np.array([25,50 , 85])
    perm = pd.read_csv(file)
    perm=perm.fillna(0)
    print(perm)
    perm['total'] = perm['dangerous']+perm['signature']+perm['normal']+perm['customized']
    perm['pct_dgr'] = round((perm['dangerous']/perm['total'])*100,2)
    perm['pct_nrm'] = round((perm['normal']/perm['total'])*100,2)
    perm['pct_sgt'] = round((perm['signature']/perm['total'])*100,2)
    perm['pct_cst'] = round((perm['customized']/perm['total'])*100,2)

    pct_dgr = perm['pct_dgr']
    pct_dgr_ecdf = sm.distributions.ECDF(pct_dgr) 
    pct_dgr_x = np.linspace(min(pct_dgr), max(pct_dgr))
    pct_dgr_y = pct_dgr_ecdf(pct_dgr_x)
    pct_dgr_val = np.percentile(pct_dgr, percentiles)

    pct_nrm = perm['pct_nrm']
    pct_nrm_ecdf = sm.distributions.ECDF(pct_nrm) 
    pct_nrm_x = np.linspace(min(pct_nrm), max(pct_nrm))
    pct_nrm_y = pct_nrm_ecdf(pct_nrm_x)
    pct_nrm_val = np.percentile(pct_nrm, percentiles)

    pct_sgt = perm['pct_sgt']
    pct_sgt_ecdf = sm.distributions.ECDF(pct_sgt) 
    pct_sgt_x = np.linspace(min(pct_sgt), max(pct_sgt))
    pct_sgt_y = pct_sgt_ecdf(pct_sgt_x)
    pct_sgt_val = np.percentile(pct_sgt, percentiles)

    pct_cst = perm['pct_cst']
    pct_cst_ecdf = sm.distributions.ECDF(pct_cst) 
    pct_cst_x = np.linspace(min(pct_cst), max(pct_cst))
    pct_cst_y = pct_cst_ecdf(pct_cst_x)
    pct_cst_val = np.percentile(pct_cst, percentiles)

    fig = plt.figure(figsize=(5,4))
    plt.plot(pct_dgr_x, pct_dgr_y*100, linestyle='--', lw = 2,color='red')
    plt.plot(pct_nrm_x, pct_nrm_y*100, linestyle='--', lw = 2,color='green')
    plt.plot(pct_sgt_x, pct_sgt_y*100, linestyle='--', lw = 2,color='blue')
    plt.plot(pct_cst_x, pct_cst_y*100, linestyle='--', lw = 2,color='orange')
    plt.legend(("Dangerous", "Normal","Signature","Customized"))
    plt.xlabel('Percentage of Permission Level', size = 10)
    plt.ylabel('ECDF', size = 10)
    # plt.plot(pct_dgr_val, percentiles, marker='o', color='red',linestyle='none')
    # plt.plot(pct_nrm_val, percentiles, marker='o', color='red',linestyle='none')
    # plt.plot(pct_sgt_val, percentiles, marker='o', color='red',linestyle='none')
    # plt.plot(pct_cst_val, percentiles, marker='o', color='red',linestyle='none')
    fig.savefig(write_path)
    plt.show()

def customized_permission(file,write_path):
    percentiles = np.array([25,50 , 85])
    perm = pd.read_csv(file)
    perm=perm.fillna(0)
    # print(perm)

    cst_perm = perm[perm['level']=='customized'].groupby(['permission'])['permission'].count().reset_index(name='count').sort_values(by=('count'),ascending=False)
    # print(cst_perm[cst_perm['count']>2])
    print(cst_perm.head(55))

    perm_name = cst_perm['permission'].head(20)
    count = cst_perm['count'].head(20)
    fig = plt.figure(figsize=(5,7))
    plt.xticks(rotation='vertical',fontsize=10)
    plt.bar(perm_name, count)
    plt.ylabel('Parameter',fontsize=10)
    plt.xlabel('# of Apps',fontsize=10)
    plt.tight_layout()
    # fig.savefig(plot_path)
    plt.show()

def not_available_permission(file,write_path):
    percentiles = np.array([25,50 , 85])
    perm = pd.read_csv(file)
    perm=perm.fillna(0)
    # print(perm)

    cst_perm = perm[perm['level']=='"N/A"'].groupby(['permission'])['permission'].count().reset_index(name='count').sort_values(by=('count'),ascending=False)
    # print(cst_perm[cst_perm['count']>2])
    print(cst_perm.head(55))

    perm_name = cst_perm['permission'].head(20)
    count = cst_perm['count'].head(20)
    fig = plt.figure(figsize=(5,7))
    plt.xticks(rotation='vertical',fontsize=10)
    plt.bar(perm_name, count)
    plt.ylabel('Parameter',fontsize=10)
    plt.xlabel('# of Apps',fontsize=10)
    plt.tight_layout()
    # fig.savefig(plot_path)
    plt.show()

def main():
    perm_plot = write_path+'permission.pdf'
    permission_plot(permission_sum_per_app_path,perm_plot)

    # pct_plot = write_path+'permission_percentage.pdf'
    # percentage_plot(permission_sum_per_app_path,pct_plot)


if __name__=='__main__':
    main()