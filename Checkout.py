# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import urllib2
import urllib
from bs4 import BeautifulSoup as bs
import requests
import json


qty=1
testlink='https://shop.bdgastore.com/collections/new-arrivals/products/wh-x-hal-eqt-running-support-93'
variant='28011319944'

testlink2='https://www.blendsus.com/collections/new-arrivals/products/vans-vault-x-horween-leathers-old-skool-cup-lx-navy'
variant2='28781399617'
session=requests.session()
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0',}
#headers={'User-Agent','Mozilla/5.0 (Linux; U; Android 4.1.1; en-gb; Build/KLP) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30'}

def add_to_cart(link,var):
    site = link.split('/')[2]
    payload=link_prep(link,var)
    response=session.post('http://' + site + '/cart/add.js', data=payload, headers=headers)
    response.raise_for_status()
    cart = session.get('http://' + site + '/cart')
    ##soup = bs(cart.content, 'html.parser')
    #cart_count = soup.find('span', 'cartcount').text
    #print('{} item added to cart'.format(cart_count))
    check_out(link)

def link_prep(link,var):
    page_load=session.get(link)
    soup=bs(page_load.text,'html.parser')
    botkey=soup.find(id='key')
    if botkey == None:
        payload={
            'id': var,
            'quantity':'1'
        }
    else:
        payload={
            'id': var,
            'quantity':'1',
            botkey['name'].encode('utf-8'): botkey['value'].encode('utf-8')
        }
    print payload
    return payload

    # site = link.split('/')[2]
    # page_load=urllib2.urlopen(link)
    # soup=BeautifulSoup(page_load,'html.parser')
    # botkey=soup.find(id="key")
    # if botkey == None:
    #     pass
    #     print 'no botkey'
    #     atclink = 'http://' + site + '/cart/add.js?id=%s&quantity=%s' % (str(var), str(qty))
    # else:
    #     param={botkey['name']:botkey['value']}
    #     add_on=urllib.urlencode(param)
    #     atclink = 'http://' + site + '/cart/add.js?id=%s&quantity=%s&%s' % (str(var), str(qty),str(add_on))
    # print atclink
    # checkout_link='http://' + site + '/checkout'

def check_out(link):
    with open('userinfo.json') as user_data:
        userinfo=json.load(user_data)

    site = link.split('/')[2]
    print('checking out')
    cart_url = 'http://' + site + '/checkout'
    response=session.get(cart_url)
    soup=bs(response.text,'html.parser')
    print soup
    exit()
    form = soup.find('form', {'class': 'edit_checkout'})

    payload = {
        '_method': 'patch',
        'authenticity_token': form.find('input', {'name': 'authenticity_token'})['value'],
        'button': '',
        'checkout[client_details][browser_height]': '728',
        'checkout[client_details][browser_width]': '1280',
        'checkout[client_details][javascript_enabled]': '0',
        'checkout[email]': userinfo['email'],
        'checkout[shipping_address][address1]': userinfo['shipping_address_1'],
        'checkout[shipping_address][address2]': '',
        'checkout[shipping_address][city]': userinfo['shipping_city'],
        'checkout[shipping_address][country]': userinfo['shipping_country'],
        'checkout[shipping_address][first_name]': userinfo['first_name'],
        'checkout[shipping_address][last_name]': userinfo['last_name'],
        'checkout[shipping_address][phone]': userinfo['phone_number'],
        'checkout[shipping_address][province]': ',,' + userinfo['shipping_state'],
        'checkout[shipping_address][zip]': userinfo['shipping_zip'],
        'previous_step': 'contact_information',
        'remember_me': 'false',
        'step': 'shipping_method',
        'utf8': '✓'
    }

    response = session.post('http://' + site  + form['action'], data=payload, headers=headers)  # customer info
    soup = bs(response.text, 'html.parser')
    print soup
    print 'shipping'


if __name__ == '__main__':
    global site
    #add_to_cart(testlink,variant)
    add_to_cart(testlink2,variant2)
