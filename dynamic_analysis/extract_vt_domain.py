import requests, urllib, json, tld, unicodedata, time, sqlite3
import os

# Parsing WHOIS dataset
def get_whois_data(text, whois_ts):
    temp = text.split("\n")
    domain = temp[0].split(":")[-1].strip()
    nserver1 = temp[1].split(":")[-1].strip()
    nserver2 = temp[2].split(":")[-1].strip()
    nstate = temp[3].split(":")[-1].strip()
    person = temp[4].split(":")[-1].strip()
    registrar = temp[5].split(":")[-1].strip()
    admin_contact = temp[6].split(":")[-1].strip()
    created_at = temp[7].split(":")[-1].strip()
    paid_till = temp[8].split(":")[-1].strip()
    source = temp[8].split(":")[-1].strip()
    return whois_ts, domain, nserver1, nserver2, nstate,person, registrar, admin_contact, created_at, paid_till, source

# Parsing malware executable on a given domain/IP
def get_detected_downloaded_samples(item, domain):     
    date = item['date'] 
    positives = item['positives']
    sha256 = item['sha256']
    total_av = item['total']
    return date, domain, positives, total_av, sha256

# Parsing suspicious/malicious URLs on this domain
def get_detected_urls(item, domain):    
    return item['scan_date'], domain, item['positives'], item['total'], item['url']

# Revealing list of resolved IPs and the timestamp
def get_ip_resolve(item, domain):
    return domain, item['ip_address'], item['last_resolved']

# Domain category
def get_cat_info(response_dict,domain):
    try:
        categories = response_dict[u'categories'][0]
    except:
        categories = "N/A"
    try:
        bit_def_cat = response_dict[u'BitDefender category']
    except:
        bit_def_cat = "N/A"
    try:
        drweb_cat = response_dict[ u'Dr.Web category']
    except:
        drweb_cat = "N/A"
    try:
        websense_cat = response_dict[u'Websense ThreatSeeker category']
    except:
        websense_cat = "N/A"
    try:
        safety_score = response_dict[u'Webutation domain info']["Safety score"]  
    except:
        safety_score = "N/A"
    try:
        adult_content = response_dict[u'Webutation domain info']["Adult content"]  
    except:
        adult_content = "N/A"
    try:
        verdict = response_dict[u'Webutation domain info']["Verdict"]  
    except:
        verdict = "N/A"

    return domain, categories, bit_def_cat, drweb_cat, websense_cat, safety_score, adult_content, verdict

# Obtaining references to malicous files/executables that refer to a given URL/domain/IP
def get_undetected_referrers(item, domain):
    return domain, item['positives'], item['total'], item['sha256']

def main():
    conn = sqlite3.connect('./vt_scan_report_.db')
    cc = conn.cursor()

    try:
        cc.execute('''CREATE TABLE whois (whois_ts TEXT, domain TEXT, whois_text TEXT)''') 
        cc.execute('''CREATE TABLE vt_detection (detection_ts TEXT, domain TEXT, npositives TEXT, nantivirustools TEXT, sha256 TEXT)''') 
        cc.execute('''CREATE TABLE domain_info (domain, category TEXT, bitdef_cat, drweb_cat TEXT, websense_cat TEXT, safety_score TEXT, adult_content TEXT, verdict TEXT)''') 
        cc.execute('''CREATE TABLE malicious_url_on_domain (scan_date TEXT, domain TEXT, npositives TEXT, nantivirustools TEXT, url TEXT)''')
        cc.execute('''CREATE TABLE ip_resolution (domain TEXT, resolved_to_ip TEXT, resolve_ts TEXT)''')
        cc.execute('''CREATE TABLE undetected_referrer_samples(domain TEXT, npositives TEXT, nantivirustools TEXT, sha256 TEXT )''')
    except:
        pass

    # Reading result from VT domain scan 
    domain_res_path = '/home/budi/crypto_project/vt_domain_result'
  
    count = 0
    for roots,dirs,files in os.walk(domain_res_path): 
        for domain in files:
            loc = roots+'/'+domain
            with open (loc,'r') as fl:
                data = fl.read()
                response_dict = json.loads(data)

            try:
                cc.execute("INSERT INTO domain_info VALUES (?,?,?,?,?,?,?,?)", get_cat_info(response_dict, domain)) 
                conn.commit()
            except:
                pass
            # some VT lookups do not have whois data
            try:
                if 'whois_timestamp' in response_dict.keys() and u'whois' in response_dict.keys():
                    cc.execute("INSERT INTO whois VALUES(?,?,?)", (response_dict['whois_timestamp'],domain, response_dict['whois']))
                    conn.commit
            
                if 'detected_downloaded_samples' in response_dict.keys():
                    for item in response_dict['detected_downloaded_samples']:
                        cc.execute("INSERT INTO vt_detection VALUES (?,?,?,?,?)", get_detected_downloaded_samples(item, domain)) 
                        conn.commit()
                elif 'detected_communicating_samples' in response_dict.keys():
                    for item in response_dict['detected_communicating_samples']:
                        cc.execute("INSERT INTO vt_detection VALUES (?,?,?,?,?)", get_detected_downloaded_samples(item, domain)) 
                        conn.commit()
            
                if u'detected_urls' in response_dict.keys():
                    for item in response_dict[u'detected_urls']:
                        cc.execute("INSERT INTO malicious_url_on_domain VALUES (?,?,?,?,?)", get_detected_urls(item, domain)) 
                        conn.commit()
                
                if u'resolutions' in response_dict.keys():
                    for item in response_dict[u'resolutions']:
                        #print get_ip_resolve(domain, item)    
                        cc.execute("INSERT INTO ip_resolution VALUES (?,?,?)", get_ip_resolve(item, domain)) 
                        conn.commit()
                if u'undetected_referrer_samples' in response_dict.keys():
                    for item in response_dict[u'undetected_referrer_samples']:
                        cc.execute('''INSERT INTO undetected_referrer_samples VALUES(?,?,?,?)''',get_undetected_referrers(item, domain))
                        conn.commit()
                elif u'undetected_downloaded_samples' in response_dict.keys():
                    for item in response_dict[u'undetected_downloaded_samples']:
                        cc.execute('''INSERT INTO undetected_referrer_samples VALUES(?,?,?,?)''',get_undetected_referrers(item, domain))
                        #print get_undetected_referrers(item, domain)
                        conn.commit()
            except:
                pass
            # With non-academic API we can issue only 4 requests per minute, so we have waiting time of 16 sec
            # TODO: replace 16sec to 4.25sec once we get academic API from VT.
            #time.sleep(4.25)
            print ("%s:: %s"% (count, domain))
            count += 1
        
        cc.close()

if __name__ == "__main__":
    
    main()