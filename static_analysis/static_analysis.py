"""
    This script is used to conduct static analysis in mobile apps including:
    - apkid analysis
    - certificate analysis
    - permission extractor
    - exported component extractor
"""

import os,shutil
import json
import pandas as pd
import csv
import subprocess
from apkid_analysis import apkid_analysis
from check_jarsigner import check_keytool
from permission_level import find_permission_level
from manifest_extractor import permission_ex
from manifest_extractor import exported_activity_ex, exported_service_ex, exported_receiver_ex, exported_provider_ex
from manifest_extractor import activity_ex, service_ex, receiver_ex, provider_ex
from library_extractor import check_lib
from vt_work import search_vt_report,vt_upload,vt_find_positive
import time

# selected_app_id = '/home/budi/crypto_project/crypto_code/static_analysis/test.csv'
selected_app_id = '/home/budi/crypto_project/crypto_code/apps_screening/wallet_apps_refined_list.csv'
apps_path = '/home/budi/crypto_project/apps_list/'
report_path = '/home/budi/crypto_project/crypto_code/static_analysis/report/'
# decompiled_path = '/home/budi/crypto_project/decompiled_app/'
decompiled_path = "/media/budi/Seagate Expansion Drive/crypto_project/decompiled_apps/"
vt_result_path = '/home/budi/crypto_project/vt_result/'
temp_path = '/home/budi/crypto_project/temp_path/'

def check_existing_result(result_path):
    file_list=[]
    for root,dirs,files in os.walk(result_path):
        for file in files:
            file_list.append(file.rstrip('.txt'))

    return(file_list)

def check_file(file_name,path):
    status = False
    for roots,dirs,files in os.walk(path):
        for file in files:
            if file_name in file:
                status = True
    return status

  
def apkid_sumarize(app_list_path,apps_path,report_path):
    apkid_result =[]
    apkid_detail = []
    with open (app_list_path,'r') as apps_list:
        for item in apps_list:
            item = item.strip('\n')
            apk_path = apps_path+item+'.apk'
            status = check_file(item,apps_path)
            if status == True:
                # print(apps_path)
                match_list = apkid_analysis(apk_path)
                anti_vm = False
                obfuscator= False
                anti_debug= False
                anti_disassembly= False
                manipulator=packer = False
                for x in match_list:
                    apkid_detail.append(x)
                    if 'anti_vm' in x['types']:
                        anti_vm = True
                    elif 'obfuscator' in x['types']:
                        obfuscator = True
                    elif 'anti_debug' in x['types']:
                        anti_debug = True
                    elif 'anti_disassembly' in x['types']:
                        anti_disassembly = True
                    elif 'packer' in x['types']:
                        packer = True
                    elif 'manipulator' in x['types']:
                        manipulator = True
                
                apkid_result.append({'app_name':item,'anti_vm':anti_vm,'obfuscator':obfuscator,'anti_debug':anti_debug,'anti_disassembly':anti_disassembly,
                'manipulator':manipulator,'packer':packer})
           
            else :
                print('apk file does not available')

    result_string = app_list_path.split('/')
    result_string = result_string[-1]

    sum_path = report_path+'apkid_sum_'+result_string
    detail_path = report_path+'apkid_detail_'+result_string
    write_to_csv(apkid_result,sum_path)
    write_to_csv(apkid_detail,detail_path)
    
def write_to_csv(file_name,file_path):
    to_write = pd.DataFrame(file_name)
    to_write.to_csv(file_path,index=False)

def jarsigner_summarize(app_list_path,apps_path,report_path):
    jar_sum =[]
    jar_detail = []
    with open (app_list_path,'r') as apps_list:
        for item in apps_list:
            item = item.strip('\n')
            apk_path = apps_path+item+'.apk'
            status = check_file(item,apps_path)
            if status == True:
                match_list = check_keytool(apk_path)
                jar_detail.append(match_list)           
            else :
                print(item+' apk file does not available')

    result_string = app_list_path.split('/')
    result_string = result_string[-1]

    detail_path = report_path+'keytool_detail_'+result_string
    write_to_csv(jar_detail,detail_path)

    sum_path = report_path+'keytool_sum_'+result_string.replace('csv','txt')
    sum_keytool = pd.DataFrame(jar_detail)
    signature = sum_keytool.groupby(['signature'])['signature'].count().reset_index(name = 'sig_count')
    key_length = sum_keytool.groupby(['key_length'])['key_length'].count().reset_index(name='key_count')
    signature = signature.to_string()
    key_length = key_length.to_string()
    with open (sum_path,'w') as fl:
        for line in signature:
            fl.write(line)
        fl.write('\n')
    with open (sum_path,'a') as fl:
        for line in key_length:
            fl.write(line)

def extract_apk(apk_path,decompiled_path,temp_path):
    package_name = apk_path.split('/')
    package_name= package_name[-1]
    print('Decompiling '+package_name)
    apk_path = apk_path+'.apk'
    os.chdir(temp_path)
    shutil.copy2(apk_path,temp_path)
    # dec_folder = decompiled_path+package_name
    # os.system('mkdir '+dec_folder)
    comm  = 'apktool d -f '+package_name+'.apk'
    os.system(comm)
    time.sleep(1)
    shutil.move(temp_path+package_name,decompiled_path)
    time.sleep(1)
    os.remove(temp_path+package_name+'.apk')
    time.sleep(1)

# def extract_apk(apk_path,decompiled_path):
#     package_name = apk_path.split('/')
#     package_name= package_name[-1]
#     print('Decompiling '+package_name)
#     apk_path = apk_path+'.apk'
#     dec_folder = decompiled_path+package_name
#     os.system('mkdir '+dec_folder)
#     comm  = 'apktool d -f '+apk_path+' -o '+dec_folder
#     os.system(comm)

def check_decompiled(item,decompiled_path):
    status = False
    for roots,dirs,files in os.walk(decompiled_path):
        if item in dirs:
            return True
    return status

def check_manifest(manifest_path):
    status = False
    path = manifest_path.replace('/AndroidManifest.xml','')
    for roots,dirs,files in os.walk(path):
        if 'AndroidManifest.xml' in files:
            status = True
    return status

def permission_sumarize(apps_list,decompiled_path,apk_path,report_path,temp_path):
    no_manifest=[]
    permission_level=[]
    with open(apps_list,'r') as app_list:
        for item in app_list:
            item = item.strip('\n')
            decom_status = check_decompiled(item,decompiled_path)
            if decom_status == False:
                print('Decompiled Folder Not available')
                print('Decompiling : '+item)
                apk_file_path = apk_path+item
                extract_apk(apk_file_path,decompiled_path,temp_path)
            manifest_path = decompiled_path+item+'/AndroidManifest.xml'
            mfs_status = check_manifest(manifest_path)           
            if mfs_status == True:
                print('Extracting permission of : '+item)
                permission_list = permission_ex(manifest_path)
                permission_level_list = find_permission_level(permission_list) 
                for perm in permission_level_list:
                    perm_item = {'app_id':item,'permission':perm['permission'],'level':perm['level']}
                    permission_level.append(perm_item)
            else:
                no_manifest.append(item)
                print('No Manifest available for :'+item)
                # perm_item = {'app_id':item,'permission':'not found','level':'not found'}
                # permission_level.append(perm_item)
    
    """ Summarizing detail permission"""
    file_sufix = apps_list.split('/')
    file_sufix=file_sufix[-1]
    perm_detail_path = report_path+'permission_detail_'+file_sufix
    write_to_csv(permission_level,perm_detail_path)

    """ Summarizing permission per app"""
    df_perm_detail = pd.DataFrame(permission_level)
    df_sum_app = df_perm_detail.groupby(['app_id','level'])['level'].count().unstack().reset_index()
    # print(df_sum_app)
    perm_sum_per_app_path = report_path+'permission_sum_per_app_'+file_sufix
    write_to_csv(df_sum_app,perm_sum_per_app_path)

    """Summarizing permission per access level"""
    df_sum_total = df_perm_detail.groupby(['level'])['level'].count().reset_index(name='count')
    print(df_sum_total)
    perm_sum_total = report_path+'permission_sum_total_'+file_sufix
    write_to_csv(df_sum_total,perm_sum_total)

    return permission_level,no_manifest

def exported_component_summarize(apps_list,decompiled_path,apk_path,report_path):
    no_manifest=[]
    component_list=[]
    with open(apps_list,'r') as app_list:
        for item in app_list:
            item = item.strip('\n')
            decom_status = check_decompiled(item,decompiled_path)
            if decom_status == False:
                print('Decompiled Folder Not available')
                print('Decompiling : '+item)
                apk_file_path = apk_path+item
                extract_apk(apk_file_path,decompiled_path)
            manifest_path = decompiled_path+item+'/AndroidManifest.xml'
            mfs_status = check_manifest(manifest_path)
            print('Checking Exported Component : '+item)
            if mfs_status == True:
                ex_act_list = exported_activity_ex(manifest_path)
                for e_act in ex_act_list:
                    component_list.append({'app_id':item,'com_type':'exp_activity','act_name':e_act}) 
                ex_serv_list = exported_service_ex(manifest_path)
                for e_serv in ex_serv_list:
                    component_list.append({'app_id':item,'com_type':'exp_service','act_name':e_serv}) 
                ex_rec_list = exported_receiver_ex(manifest_path)
                for e_rec in ex_rec_list:
                    component_list.append({'app_id':item,'com_type':'exp_receiver','act_name':e_rec}) 
                ex_prov_list = exported_provider_ex(manifest_path)
                for e_prov in ex_prov_list:
                    component_list.append({'app_id':item,'com_type':'exp_provider','act_name':e_prov}) 
                act_list = activity_ex(manifest_path)
                for act in act_list:
                    component_list.append({'app_id':item,'com_type':'activity','act_name':act}) 
                serv_list = service_ex(manifest_path)
                for serv in serv_list:
                    component_list.append({'app_id':item,'com_type':'service','act_name':serv}) 
                rec_list = receiver_ex(manifest_path)
                for rec in rec_list:
                    component_list.append({'app_id':item,'com_type':'receiver','act_name':rec}) 
                prov_list = provider_ex(manifest_path)
                for prov in prov_list:
                    component_list.append({'app_id':item,'com_type':'provider','act_name':prov}) 
    
    """ Summarizing detail component analysis"""
    file_sufix = apps_list.split('/')
    file_sufix=file_sufix[-1]
    exp_comp_detail_path = report_path+'exported_component_detail_'+file_sufix
    write_to_csv(component_list,exp_comp_detail_path)

    """Summarizing exported component per apps"""
    df_comp = pd.DataFrame(component_list)
    exp_comp_sum = df_comp.groupby(['app_id','com_type'])['com_type'].count().unstack().reset_index()
    exp_comp_sum['pct_exp_act'] = round((exp_comp_sum['exp_activity']/exp_comp_sum['activity']),2)
    exp_comp_sum['pct_exp_serv'] = round((exp_comp_sum['exp_service']/exp_comp_sum['service']),2)
    exp_comp_sum['pct_exp_rec'] = round((exp_comp_sum['exp_receiver']/exp_comp_sum['receiver']),2)
    exp_comp_sum['pct_exp_prov'] = round((exp_comp_sum['exp_provider']/exp_comp_sum['provider']),2)
    exp_comp_sum_path = report_path+'exported_component_sum_per_app_'+file_sufix
    write_to_csv(exp_comp_sum,exp_comp_sum_path)
    print(exp_comp_sum)

    """Summarizing exported component per component"""
    exp_comp_total = df_comp.groupby(['com_type'])['com_type'].count().reset_index(name='count')
    exp_comp_total_path = report_path+'exported_component_total_'+file_sufix
    write_to_csv(exp_comp_total,exp_comp_total_path)
    # print(exp_comp_total)
    return component_list
    
def third_party_lib_summarize(apps_list,decompiled_path,report_path):
    third_party_lib_list=[]
    with open(apps_list,'r') as app_list:
        for item in app_list:
            item = item.strip('\n')
            decom_status = check_decompiled(item,decompiled_path)
            if decom_status == True:
                try:
                    folder_path = decompiled_path+item
                    # print(folder_path)
                    lib_list = check_lib(folder_path)
                    for x in lib_list:
                        app_id = {'app_id':item}
                        x_item = dict(app_id,**x)
                        # print(x_item)
                        third_party_lib_list.append(x_item)
                except:
                    pass
            else:
                print(item+' Decompiled folder not found')

    """ Summarizing detail third party libraries"""
    file_sufix = apps_list.split('/')
    file_sufix=file_sufix[-1]
    lib_detail_path = report_path+'library_detail_'+file_sufix
    write_to_csv(third_party_lib_list,lib_detail_path)

    """ Summarizing third party libraries per apps"""
    lib_sum_per_app_path = report_path+'library_sum_per_app_'+file_sufix
    df_lib = pd.DataFrame(third_party_lib_list)
    print(df_lib)
    lib_per_app = df_lib.groupby(['app_id'])[['TargetedAds','MobileAnalytics','AnyTrackingLibrary','Analytics']].sum().reset_index()
    # print(lib_per_app)
    write_to_csv(lib_per_app,lib_sum_per_app_path)
    
    """Summarizing third party library per name"""
    lib_per_name = df_lib.groupby(['lib_name'])['lib_name'].count().reset_index(name='count').sort_values('count',ascending=False)
    lib_per_name_path = report_path+'lib_per_name_'+file_sufix
    write_to_csv(lib_per_name,lib_per_name_path)
    print(lib_per_name)
    return third_party_lib_list

def check_vt_status(item,vt_report_path):
    for roots,dirs,files in os.walk(vt_report_path):
        if item in files:
            return True
        else:
            return False

def isFileSizeLessthan32MB(path):
    if os.path.getsize(path) < 32000000:
        return True
    else:
        return False

def vt_scan(apps_list,vt_report_path,apps_path,report_path):
    exceed_32mb_list =[]
    vt_positive_result_list = []
    with open(apps_list,'r') as app_list:
        for item in app_list:
            item = item.strip('\n')
            vt_status = check_vt_status(item,vt_report_path)
            vt_result_apk_path = vt_report_path+item
            if vt_status == False:
                apk_path = apps_path+item+'.apk'
                res = search_vt_report(apk_path)
                # no_result = 'queued or pending'
                try:
                    if res['response_code']==0:
                        if isFileSizeLessthan32MB == True:
                            upload_res = vt_upload(apk_path)
                            print(upload_res)
                        else:
                            print('The File size is exceeding 32 MB')
                            exceed_32mb_list.append(item)
                    else:
                        print('Write result to disk :'+item)
                        with open (vt_result_apk_path,'w') as vtj:
                            try:
                                json.dump(res,vtj)
                            except:
                                print('Cannot decode to json format')
                except:
                    print(res)
            else:
                vt_positive = vt_find_positive(vt_result_apk_path)
                for positive in vt_positive:
                    app_id = {'app_id':item}
                    item_positive = dict(app_id,**positive)
                    vt_positive_result_list.append(item_positive)
            time.sleep(10)

    """ Summarizing detail virus total positive result"""
    file_sufix = apps_list.split('/')
    file_sufix=file_sufix[-1]
    vt_detail_path = report_path+'vt_positive_detail_'+file_sufix
    # print(vt_detail_path)
    write_to_csv(vt_positive_result_list,vt_detail_path)

    """ Summarizing positive virus total per apps"""
    vt_sum_per_app = report_path+'vt_sum_per_app_'+file_sufix
    df_vt = pd.DataFrame(vt_positive_result_list)
    vt_per_app = df_vt.groupby(['app_id'])['app_id'].count().reset_index(name='count')
    print(vt_per_app)
    write_to_csv(vt_per_app,vt_sum_per_app)
   
    return vt_positive_result_list
def main():

    # not_found =[]
    # with open (selected_app_id,'r') as apps_list:
    #     for item in apps_list:
    #         item = item.strip('\n')
    #         status = check_file(item,apps_path)
    #         # print(item)
    #         if status == False:
    #             not_found.append(item.strip('\n'))
    #             print(item)

    # not_found_path = report_path+'not_found_app.txt'
    # with open(not_found_path,'w') as nf:
    #     for line in not_found:
    #         nf.write(line+'\n')            
    perm_level = permission_sumarize(selected_app_id,decompiled_path,apps_path,report_path,temp_path)    
    # exp_comp = exported_component_summarize(selected_app_id,decompiled_path,apps_path,report_path)    
    # for x in exp_comp:
    #     print(x)
    # libraries = third_party_lib_summarize(selected_app_id,decompiled_path,report_path)    
    # for x in libraries:
    #     print(x)
    # for x in perm_level[0]:
    #     print(x)
    # apkid_sumarize(selected_app_id,apps_path,report_path)    
    # jarsigner_summarize(selected_app_id,apps_path,report_path)
    # vt_positive = vt_scan(selected_app_id,vt_result_path,apps_path,report_path)
    # print(vt_positive)
if __name__ == "__main__":
    main()
