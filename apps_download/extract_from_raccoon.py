# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 13:14:29 2021

@author: 45076189
"""

import os

raccoon_path = 'C:/Users/45076189/Documents/Raccoon/content/apps'
destination_folder = 'C:/Users/45076189/crypto_project/extracted_apk'

def extract_raccoon_dir(raccoon_path):
    list_dir=[]
    for roots,dirs,files in os.walk(raccoon_path):
        for dir in dirs:
            item_dir = roots+'/'+dir
            list_dir.append({'dir':item_dir,'package_name':dir})
        # print(item_dir)
    return list_dir
        
def extract_package_name(package_path,package_name,destination_folder):
    for roots,dirs,files in os.walk(package_path):
        for file in files:
            if package_name in file:
                source = package_path+ '/'+file
                # source=source.replace('/','\\')
                destination = destination_folder+'/'+package_name+'.apk'
                # destination = destination.replace('/', '\\')
                cmd = 'copy '+source+' '+destination
                print(cmd)
                os.system(cmd)
def main():
    res = extract_raccoon_dir(raccoon_path)
    for item in res:
        # print(item['dir'])
        extract_package_name(item['dir'], item['package_name'], destination_folder)

if __name__=='__main__':
    main()
        