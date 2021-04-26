# sudo pip install urllib3
import urllib3

# pip install sets
# from sets import Set

# Install bs4

# sudo pip install bs4
# from bs4 import BeautifulSoup

from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import requests



def findId(source):
    ids = []
    soup =  BeautifulSoup(source,"html.parser")
    divs = soup.findAll('div', {'class':'b8cIId ReQCgd Q9MA7b'})
    print(divs)
    ids_r =  []
    for item in divs:
        try:
            ids_r.append(item.find('a').attrs['href'].split('id=')[-1])
        except:
            print("some errors occured with findID()")
            pass
    return ids_r

# def get_source(url):
#     request = urllib3.Request('https://play.google.com/store/apps/details?id='+url) #urllib2.urlopen(url)
#     print(request)
#     page_source = urllib3.urlopen(request).read()
#     return page_source



def get_source(url):
    page_source = requests.get('https://play.google.com/store/apps/details?id='.format(url), headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.5 (KHTML, like Gecko) '
                      'Version/9.1.2 Safari/601.7.5 '
    }).text
    
    return page_source


def search(source, depth):
    if depth==1:
        return
    # print(source, depth)

    try:
        page_source = get_source(source)
        # print(page_source)
        links = set(findId(page_source))
    except:
        print('some error encountered')
        return

    global urls
    for link in links:
        if link not in urls:
            urls = urls|set([link])        

    for link in urls:
        search(link,depth+1)



if __name__ =="__main__": 

    # Seed App-IDs
    # start_links = ['com.moonbag.wallet',
    # 'com.coinbase.pro', 
    # 'com.blockchainpluswallet.plus_wallet_app',
    # 'io.totalcoin.wallet', 
    # 'com.blocktrail.mywallet']

    start_links = 'io.hashshiny.fanhui.qukuai'


    # urls = Set(start_links)
    urls = set(start_links)

    count = 0
    for start_link in start_links:
        print ("%s : Total apps : %s " % (count, len(urls)))
        search(start_link,0)
        count += 1

    fo = open("gcrawler_output_crypto_wallet.txt", "w")
    for item in urls:
        print(item)
        fo.write(item+"\n")
    fo.close()