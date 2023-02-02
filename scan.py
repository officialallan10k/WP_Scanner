import requests,json,re,time,sys
from random_useragent import RANDOM_USER_AGENT
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore,init
init()
Dgreen = Fore.LIGHTGREEN_EX
Lgreen = Fore.LIGHTGREEN_EX
Lyellw = Fore.LIGHTYELLOW_EX
Lred = Fore.LIGHTRED_EX
Lcyan = Fore.LIGHTCYAN_EX
meron = []
wala = []
def multikapogian(defmikey,values):
	with ThreadPoolExecutor(max_workers=20) as executor:
		for value in values:
			executor.submit(defmikey, value)

def version_parser(v):
    versionPattern = r'\d+(=?\.(\d+(=?\.(\d+)*)*)*)*'
    regexMatcher = re.compile(versionPattern)
    return regexMatcher.search(v).group(0)
    
def user_finder(new_u) :

    new_url2 = new_u+'/wp-json/wp/v2/users'
    
    headers = {"user-agent":RANDOM_USER_AGENT}
    
    r2 = requests.get(new_url2,headers=headers)
    
    if r2.status_code == 200 :
        print(Dgreen+'\n[+] Enumerating usernames : \n')
        #time.sleep(1.3)
        data = json.loads(r2.text)
        for info in data :
            print(Lgreen+' [*] Username Found : {}'.format(info['slug']))
            #time.sleep(0.2)
    else :
            print(Lyellw+'\n[-] Usernames Not Found ')

#--------------------------------------------

def _scan(plugin):
    host = org_url + plugin
    headers = {"user-agent":RANDOM_USER_AGENT}
    r = requests.get(host, headers=headers)
    f = open("found.txt", "a")
    if r.status_code == 200:
      
      try:
        rVersion = requests.get(host + "/readme.txt", headers=headers)
        #rVersion = rVersion.text.split("Stable tag: ")[1].split("\n")[0]
        #rVersion = rVersion.text.split("== Changelog ==")[1].split("=")[1].split("=")[0].lower().replace("version","")
        rVersion = version_parser(rVersion.text.split("== Changelog ==")[1].split("=")[1].split("=")[0].lower().replace("version",""))
        meron.append(str(r.status_code) + ' ' + host + rVersion)
        print(Lgreen + ' [+] Found [+] ' + str(r.status_code) + ' ' + host + ' Version: ' + rVersion)
        f.write(host + ' Version: ' + rVersion + '\n')
      except:
        meron.append(str(r.status_code) + ' ' + host)
        print(Lgreen + ' [+] Found [+] ' + str(r.status_code) + ' ' + host)
        f.write(host + '\n')
    else:
      pass
      #wala.append(str(r.status_code) + ' ' + host)
      #print(Lred + ' [-] Not Found [-] ' + str(r.status_code) + ' ' + host)
    f.close

#--------------------------------------------

def adminpanel_finder(org_url) :
    
    urlA = org_url+'/wp-login.php?action=lostpassword&error=invalidkey'
    uagent = {"user-agent":RANDOM_USER_AGENT}
    
    r3 = requests.get(urlA,headers=uagent)

    if r3.status_code == 200 :
        r3data = r3.text
        pagesoup = BeautifulSoup(r3data,'html.parser')
        ptag = pagesoup.findAll("p",{"id":"nav"})
        
        if len(ptag) > 0 :
            for ptags in ptag :
                for atags in ptags.find_all('a') :
                    if 'Log in' in atags :
                        admin_url = atags['href']
                    else :
                        print(Lyellw+'\n[-] Admin panel not found ')

            print(Lgreen+'\n[+] Admin panel found - ',admin_url)
        
        else :
            print(Lyellw+'\n[-] Admin panel not found ')
    else :
        print(Lyellw+'\n[-] Admin panel not found ')


#---------------------------------------------

banner = """
 █ █ █ █▀█   █▀ █▀▀ ▄▀█ █▄ █ █▄ █ █▀▀ █▀█
 ▀▄▀▄▀ █▀▀   ▄█ █▄▄ █▀█ █ ▀█ █ ▀█ ██▄ █▀▄ """
dashline = "-------------------------------------------"
author = "  [+] Coded by Allan10k   [+] v 1.1 "
description = "\n [#] An upgraded version of GH0STH4CKER - WP_Scanner [#] "
print(Lgreen+banner)
print(Lgreen+dashline)
print(Lyellw+author)
print(Lcyan+description)
print(Lgreen+dashline)

#---------------------------------------------
if 2 <= len(sys.argv):
	url = sys.argv[1]
else:
	print(Dgreen+ '\nWebsite Url (with https://) : ' + Lgreen, end="")
	url = input('')
org_url = url
roboturl = url+'/robots.txt'
feedurl = url+'/feed'
url = url+'/wp-json'

headers = {"user-agent":RANDOM_USER_AGENT}

try:
    testreq = requests.get(org_url,headers=headers)
except Exception as e:
    print(Lred+'\n[+] Website status : Error !')
else :
    print(Dgreen+'\n[+] Target : '+Lgreen+org_url)
    print(Dgreen+'\n[+] Website status : ',Lgreen+'Up')

    r = requests.get(url,headers=headers)
    rcode = r.status_code

    if rcode == 200 :

        robotres = requests.get(roboturl,headers=headers)

        if 'wp-admin' == 'wp-admin' :
            print(Dgreen+'\n[+] WordPress Detection : ',Lgreen+'Yes')

            feedres = requests.get(feedurl,headers=headers)
            contents = feedres.text
            soup = BeautifulSoup(contents,'xml')
            wpversion = soup.find_all('generator')
            if len(wpversion) > 0 :
                wpversion = re.sub('<[^<]+>', "", str(wpversion[0])).replace('https://wordpress.org/?v=','')
                print(Dgreen+'\n[+] WordPress version : ',Lgreen+wpversion)
            else:
                rnew = requests.get(org_url,headers=headers)
                if rnew.status_code == 200 :
                    newsoup = BeautifulSoup(rnew.text,'html.parser')
                    generatorTAGS = newsoup.find_all('meta',{"name":"generator"})
                    for metatags in generatorTAGS :     
                        if "WordPress" in str(metatags) :
                            altwpversion = metatags['content']
                            altwpversion = str(altwpversion).replace('WordPress','')
                            print(Dgreen+'\n[+] WordPress version : ',Lgreen+altwpversion)
                else :
                    print(Lyellw+'[-] WordPress version : Not Found !')

            adminpanel_finder(org_url)
            user_finder(org_url)

            data = json.loads(r.text)
            #siteName = data['name']
            #siteDesc = data['description']
            #print(Dgreen+'\n[+] Webite name        :',Lgreen+siteName)
            #print(Dgreen+'\n[+] Webite description :',Lgreen+siteDesc)
            #plugins = data['namespaces']
            #print(plugins)
            #print(Dgreen+'\n[+] Enumerating Plugins :',end=' ')
            #plugins=list(set(plugins))
            #print('\n')
            #for i in plugins :
            #    elem = (i[:i.find('/')])
            #    print(Lgreen+' [*] ',elem) 
            #    time.sleep(0.2)
            print(Dgreen+'\n[+] Enumerating Plugins :',end=' ')
            print('\n')
            f = open('plugins.txt','rt')
            plugins = f.read()
            plugins = plugins.split('\n')
            multikapogian(_scan, plugins)
                         
            
            

        else :
            print(Lyellw+'\n[-] WordPress Detection : No')
    else :
        print(Lyellw+'\n[-] WordPress Detection : No')

print(Lcyan+'')
print('[ Thank you for using my tool ]')
