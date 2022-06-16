import pandas as pd
from pandas.io.parsers import read_csv 
import numpy as np
import statsmodels.api as sm # recommended import according to the docs
import matplotlib.pyplot as plt


exported_path = '/home/budi/crypto_project/crypto_code/static_analysis/report/exported_component_sum_per_app_wallet_apps_refined_list.csv'
write_path = '/home/budi/crypto_project/crypto_code/static_analysis/plot/'

def component_plot(file,write_path):
    percentiles = np.array([25,50 , 85])
    exported = pd.read_csv(file)
    exported=exported.fillna(0)
    # exported['activity'] = exported['activity'].apply(lambda x: [y if y <= 50 else 51 for y in x])  
    exported['activity'].where(exported['activity'] <= 50, 51, inplace=True)
    print(exported)

    act = exported['activity']
    act_ecdf = sm.distributions.ECDF(act) 
    act_x = np.linspace(min(act), max(act))
    act_y = act_ecdf(act_x)
    act_val = np.percentile(act, percentiles)

    ser = exported['service']
    ser_ecdf = sm.distributions.ECDF(ser) 
    ser_x = np.linspace(min(ser), max(ser))
    ser_y = ser_ecdf(ser_x)
    ser_val = np.percentile(ser, percentiles)

    rec = exported['receiver']
    rec_ecdf = sm.distributions.ECDF(rec) 
    rec_x = np.linspace(min(rec), max(rec))
    rec_y = rec_ecdf(rec_x)
    rec_val = np.percentile(rec, percentiles)

    prov = exported['provider']
    prov_ecdf = sm.distributions.ECDF(prov) 
    prov_x = np.linspace(min(prov), max(prov))
    prov_y = prov_ecdf(prov_x)
    prov_val = np.percentile(prov, percentiles)

    fig = plt.figure(figsize=(5,4))
    plt.plot(act_x, act_y*100, linestyle='--', lw = 2)
    plt.plot(ser_x, ser_y*100, linestyle='--', lw = 2)
    plt.plot(rec_x, rec_y*100, linestyle='--', lw = 2)
    plt.plot(prov_x, prov_y*100, linestyle='--', lw = 2)
    plt.legend(("Activity", "Service","Receiver","Provider"))
    plt.xlabel('# of Component', size = 10)
    plt.ylabel('ECDF', size = 10)
    # plt.plot(act_val, percentiles, marker='o', color='red',linestyle='none')
    # plt.plot(ser_val, percentiles, marker='o', color='red',linestyle='none')
    # plt.plot(rec_val, percentiles, marker='o', color='red',linestyle='none')
    # plt.plot(prov_val, percentiles, marker='o', color='red',linestyle='none')
    fig.savefig(write_path)
    plt.show()

def percentage_plot(file,write_path):
    percentiles = np.array([25,50 , 85])
    exported = pd.read_csv(file)
    exported=exported.fillna(0)
    print(exported)

    pct_exp_act = exported['pct_exp_act']*100
    pct_exp_act_ecdf = sm.distributions.ECDF(pct_exp_act) 
    pct_exp_act_x = np.linspace(min(pct_exp_act), max(pct_exp_act))
    pct_exp_act_y = pct_exp_act_ecdf(pct_exp_act_x)
    pct_exp_act_val = np.percentile(pct_exp_act, percentiles)

    pct_exp_ser = exported['pct_exp_serv']*100
    pct_exp_ser_ecdf = sm.distributions.ECDF(pct_exp_ser) 
    pct_exp_ser_x = np.linspace(min(pct_exp_ser), max(pct_exp_ser))
    pct_exp_ser_y = pct_exp_ser_ecdf(pct_exp_ser_x)
    pct_exp_ser_val = np.percentile(pct_exp_ser, percentiles)

    pct_exp_rec = exported['pct_exp_rec']*100
    pct_exp_rec_ecdf = sm.distributions.ECDF(pct_exp_rec) 
    pct_exp_rec_x = np.linspace(min(pct_exp_ser), max(pct_exp_rec))
    pct_exp_rec_y = pct_exp_rec_ecdf(pct_exp_rec_x)
    pct_exp_rec_val = np.percentile(pct_exp_rec, percentiles)

    pct_exp_prov = exported['pct_exp_prov']*100
    pct_exp_prov_ecdf = sm.distributions.ECDF(pct_exp_prov) 
    pct_exp_prov_x = np.linspace(min(pct_exp_ser), max(pct_exp_prov))
    pct_exp_prov_y = pct_exp_prov_ecdf(pct_exp_prov_x)
    pct_exp_prov_val = np.percentile(pct_exp_prov, percentiles)

    fig = plt.figure(figsize=(5,4))
    plt.plot(pct_exp_act_x, pct_exp_act_y*100, linestyle='--', lw = 2)
    plt.plot(pct_exp_ser_x, pct_exp_ser_y*100, linestyle='--', lw = 2)
    plt.plot(pct_exp_rec_x, pct_exp_rec_y*100, linestyle='--', lw = 2)
    plt.plot(pct_exp_prov_x, pct_exp_prov_y*100, linestyle='--', lw = 2)
    plt.legend(("Activity", "Service","Receiver","Provider"))
    plt.xlabel('Percentage of Exported Component', size = 10)
    plt.ylabel('ECDF', size = 10)
    # plt.plot(pct_exp_act_val, percentiles, marker='o', color='red',linestyle='none')
    # plt.plot(pct_exp_ser_val, percentiles, marker='o', color='red',linestyle='none')
    # plt.plot(pct_exp_rec_val, percentiles, marker='o', color='red',linestyle='none')
    # plt.plot(pct_exp_prov_val, percentiles, marker='o', color='red',linestyle='none')
    fig.savefig(write_path)
    plt.show()

def exported_plot(file,write_path):
    percentiles = np.array([25,50 , 85])
    exported = pd.read_csv(file)
    exported=exported.fillna(0)
    print(exported)

    exp_act = exported['exp_activity']
    exp_act_ecdf = sm.distributions.ECDF(exp_act) 
    exp_act_x = np.linspace(min(exp_act), max(exp_act))
    exp_act_y = exp_act_ecdf(exp_act_x)
    exp_act_val = np.percentile(exp_act, percentiles)

    exp_ser = exported['exp_service']
    exp_ser_ecdf = sm.distributions.ECDF(exp_ser) 
    exp_ser_x = np.linspace(min(exp_ser), max(exp_ser))
    exp_ser_y = exp_ser_ecdf(exp_ser_x)
    exp_ser_val = np.percentile(exp_ser, percentiles)

    exp_rec = exported['exp_receiver']
    exp_rec_ecdf = sm.distributions.ECDF(exp_rec) 
    exp_rec_x = np.linspace(min(exp_ser), max(exp_rec))
    exp_rec_y = exp_rec_ecdf(exp_rec_x)
    exp_rec_val = np.percentile(exp_rec, percentiles)

    exp_prov = exported['exp_provider']
    exp_prov_ecdf = sm.distributions.ECDF(exp_prov) 
    exp_prov_x = np.linspace(min(exp_ser), max(exp_prov))
    exp_prov_y = exp_prov_ecdf(exp_prov_x)
    exp_prov_val = np.percentile(exp_prov, percentiles)

    fig = plt.figure(figsize=(5,4))
    plt.plot(exp_act_x, exp_act_y*100, marker='o', lw = 2)
    plt.plot(exp_ser_x, exp_ser_y*100, marker='^', lw = 2)
    plt.plot(exp_rec_x, exp_rec_y*100, marker='s', lw = 2)
    plt.plot(exp_prov_x, exp_prov_y*100, marker='X', lw = 2)
    plt.legend(("Activity", "Service","Receiver","Provider"))
    plt.xlabel('# of Exported Component', size = 14)
    plt.ylabel('ECDF', size = 14)
    plt.xlim(0,max(exp_act_x))
    # plt.ylim(0,max(exp_act_y)*100)


    # plt.plot(exp_act_val, percentiles, marker='o', color='red',linestyle='none')
    # plt.plot(exp_ser_val, percentiles, marker='o', color='red',linestyle='none')
    # plt.plot(exp_rec_val, percentiles, marker='o', color='red',linestyle='none')
    # plt.plot(exp_prov_val, percentiles, marker='o', color='red',linestyle='none')
    fig.savefig(write_path)
    plt.show()

def main():
    # comp_plot = write_path+'component.pdf'
    # component_plot(exported_path,comp_plot)

    exp_plot = write_path+'exported_component.pdf'
    exported_plot(exported_path,exp_plot)

    # pct_exp_plot = write_path+'percentage_exp_comp.pdf'
    # percentage_plot(exported_path,pct_exp_plot)

if __name__=='__main__':
    main()