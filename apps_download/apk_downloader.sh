#!/bin/sh
COUNTER=0
while read apps_list
do 
	gplaycli -d $apps_list
    	mv $apps_list.apk /home/budi/crypto_project/apps_list/
	let COUNTER=COUNTER+1
	sleep 10

done < apk_list.txt
