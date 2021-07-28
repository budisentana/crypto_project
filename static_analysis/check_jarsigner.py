"""
    This script use to check the signing algorithm used by apk
    and using keytool
    keytool can detect the key length and algoritm but cannot check the signing mechanism version
    this tool also failed if the apk disabling (set to false) their version 1 signing mechanism
"""

import os
import json
import subprocess

apk_file = '/home/budi/crypto_project/sandbox/com.bitcoin.mwallet.apk'

def check_keytool(apk_file):
    print('Extracting Keytool of '+apk_file)
    res = subprocess.getoutput('keytool -printcert -jarfile '+apk_file)
    keytool_res = list(res.split('\n'))
    signature = key_length = 'error'
    for line in keytool_res:
        app_name = find_app_name(apk_file)
        if 'Signature algorithm' in line:
            signature = line.lstrip('Signature algorithm name ')
            # print(signature)
            signature = signature.lstrip(':')
            signature = signature.replace('with', ' + ').strip('\n')
        if 'Public Key' in line:
            key_length = line.lstrip('Subject Public Key Algorithm')
            key_length = key_length.lstrip(':')

    cert_item_list = {'file_name':app_name,'signature':signature,'key_length':key_length}   
    return cert_item_list

def find_app_name(apk_file):
    split_apk = apk_file.split('/')
    app_name = split_apk[-1]
    return app_name

def main():
    keytool = check_keytool(apk_file)
    print(keytool)

if __name__ == "__main__":
    main()