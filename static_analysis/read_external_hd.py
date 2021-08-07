import os
import shutil


hdd_path = "/media/budi/Seagate Expansion Drive/crypto_project/apps_list/"
decom_path = "/media/budi/Seagate Expansion Drive/crypto_project/decompiled_apps/"
temp_path = '/home/budi/crypto_project/temp_path/'
internal_decom = '/home/budi/crypto_project/decompiled_app/'

def read_hdd(internal_decom,decom_path):
    first_level_dir = next(os.walk(internal_decom))[1]
    for item in first_level_dir:
        source_path = internal_decom+item
        destination_path = decom_path+item
        shutil.move(source_path,destination_path)

def main():
    read_hdd(internal_decom,decom_path)

if __name__=="__main__":
    main()