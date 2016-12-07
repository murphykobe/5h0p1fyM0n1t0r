import urllib2
import time
import threading
from pushover import init, Client
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil import tz
from xml.dom import minidom
import webbrowser
#token:aG87hsFjfWX7bbJDu6GDqf5dyrxnyd
#user:u5jig8iMAwXeVHMKnXssWdjGiMLVdN
#from selenium import webdriver
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC

client = Client("u5jig8iMAwXeVHMKnXssWdjGiMLVdN", api_token="aG87hsFjfWX7bbJDu6GDqf5dyrxnyd")
global hdr
hdr = {'User-Agent': 'Mozilla/5.0'}

palace='http://shop-usa.palaceskateboards.com/sitemap_products_1.xml'
ronin='http://www.ronindivision.com/sitemap_products_1.xml'
bnrb='http://burnrubbersneakers.com/sitemap_products_1.xml'
yzsp='http://shop.yeezysupply.com/sitemap_products_1.xml'
kith='http://kithnyc.com/sitemap_products_1.xml'
cncpts='http://shop.cncpts.com/sitemap_products_1.xml'
bdga='http://shop.bdgastore.com/sitemap_products_1.xml'
xbih='http://www.xhibition.co/sitemap_products_1.xml'
sole='http://soleclassics.com/sitemap_products_1.xml'
rise='http://rise45.com/sitemap_products_1.xml'
donc='http://shopjustdon.myshopify.com/sitemap_products_1.xml'
blds='http://www.blendsus.com/sitemap_products_1.xml'
blkmkt='http://www.blkmkt.us/sitemap_products_1.xml'
notre='http://www.notre-shop.com/sitemap_products_1.xml'
union='https://store.unionlosangeles.com/sitemap_products_1.xml'
nice='https://shopnicekicks.com/sitemap_products_1.xml'
kanye='http://nikepreorders.com/sitemap_products_1.xml'
unkw='http://americanrag.com/sitemap_products_1.xml'
kylie='http://shop.kyliecosmetics.com/sitemap_products_1.xml'
nomad='http://nomadshop.net/sitemap_products_1.xml'
lvsd='http://www.deadstock.ca/sitemap_products_1.xml'
havn='http://shop.havenshop.ca/sitemap_products_1.xml'
prop='http://apropersite.com/sitemap_products_1.xml'
ftsb='http://www.featuresneakerboutique.com/sitemap_products_1.xml'
slcs='http://soleclassics.com/sitemap_products_1.xml'
cbshop='http://www.cityblueshop.com/sitemap_products_1.xml'
packer='http://packershoes.com/sitemap_products_1.xml'
stafrd='http://www.saintalfred.com/sitemap_products_1.xml'
exbt='http://shop.extrabutterny.com/sitemap_products_1.xml'
dash='https://shopdashonline.com/sitemap_products_1.xml'
oth='https://offthehook.ca/sitemap_products_1.xml'
fog='https://fearofgod.com/sitemap_products_1.xml'
excu='https://shop.exclucitylife.com/sitemap_products_1.xml'


class ShopifyMonitor():

    def __init__(self):
         self.data=[]
         self.data_old=[]
         self.link_set=[]

    def update(self, site):
          self.data=[]

          urlList=[]
          timeList=[]
          nameList=[]
          xml = urllib2.urlopen(site).read()
          xmldoc = minidom.parseString(xml)
          links = xmldoc.getElementsByTagName('loc')
          for l in links[1:]:
              item=l.firstChild.nodeValue
              urlList.append(item)

          names = xmldoc.getElementsByTagName('image:title')
          for n in names[1:]:
              item=n.firstChild.nodeValue
              nameList.append(item)

          times = xmldoc.getElementsByTagName('lastmod')
          for n in times[1:]:
              item=n.firstChild.nodeValue
              temp_date = item[:10]+' '+item[11:19]
              item=UTC2EST(temp_date)
              timeList.append(item)

          unit=zip(timeList,nameList,urlList)
          #XML DOM Parsing Approach FAST!

          # temp=urllib2.urlopen(site)
          # soup = BeautifulSoup(temp, "xml")
          # #print soup
          # for url in soup.find_all('url')[1:]:
          #       #print url
          #       date = url.lastmod.string
          #       temp_temp = date[:10]+' '+date[11:19]
          #       date = UTC2EST(temp_temp)
          #       #string operation convert to est
          #       name = url.find('image'and'title').string
          #       #print name
          #       link = url.loc.string
          #       unit = (date, name, link)
          #self.data=unit.append()
          #BeatifulSoup 4 Parsing approach SLOW!

          self.data=unit
          self.data = sorted(self.data, key=lambda unit:unit[0],reverse=True)

    def link_gen(self,link,key):
        print ('*****************************************')
        load_size=urllib2.urlopen(link)
        soup=BeautifulSoup(load_size, 'xml')
        print('variant found')
        for variant in soup.find_all('variant'):

            print ('Size=%s'% variant.title.string)
            qty= variant.find('inventory-quantity')
            if qty == None:
                print('Inv_Qty Undefined')
            else:
                print ('Inv_Qty=%s'% qty.text)
            site=link.split('/')[2]
            atclink='http://'+site+'/cart/%s:1'% variant.id.string
            print (atclink)
            print ('-----------------------------------------')
            self.link_set.append(atclink)
            if key == '':
                pass
            elif key in link:
                #webbrowser.open_new_tab(atclink)
                time.sleep(0.5)

    def run(self,site,key):
          print UTC2EST(1)
          print('Initializing%s'%site)
          self.update(site)
          self.data_old=self.data
          while True:

                self.update(site)
                n=len(set(self.data)^set(self.data_old))
                #print('Count= %d'% n)

                if n==0:
                      print('No Item Found')
                      print UTC2EST(1)
                      pass
                else:
                      #print(len(self.data))
                      #print(len(self.data_old))
                      head=self.data
                      #print(len(head))
                      print head[0]
                      #if key in head[0]:
                      client.send_message(head[0][2],title=head[0][1])
                      #client.send_message(head[0][2],title=head[0][1])
                      print(str(head[0][2]))
                      xmlink= str(head[0][2])+'.xml'
                      self.link_gen(xmlink,key)
                #print n
                #print len(self.data)
                #print len(self.data_old)
                self.data_old=self.data
                #time.sleep(0)

def init_session(site,key): # site for the link of sitemap xml, key is the search keyword
    sitespf=ShopifyMonitor()
    sitethd=threading.Thread(target=sitespf.run,args=(site,key))
    sitethd.start()

def UTC2EST(zulu):
    if zulu==1:
        return str(datetime.now())
    else:
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        utc=datetime.strptime(zulu, "%Y-%m-%d %H:%M:%S")
        utc = utc.replace(tzinfo=from_zone)
        eastern = utc.astimezone(to_zone)
        return str(eastern)[:19]

if __name__ == '__main__':
    #init_session(ronin,'hoodie')
    #init_session(bdga,'')
    #init_session(packer,'boost')
    init_session(kith,'')
    #init_session(kith,'')
    #init_session(notre,'')
    #init_session(havn,'')
    #init_session(nomad,'wood')
    #init_session(blds,'')
    #init_session(kith,'')
    #init_session(bdga,'')
    #init_session(prop,'')
    #init_session(bdga,'')
    #init_session(kith,'')
    #init_session(lvsd,'')
    #init_session(cbshop,'')
    #init_session(palace,'')
    #init_session(unkw,'fear')
    #init_session(excu,'')
    #init_session(sole,'')