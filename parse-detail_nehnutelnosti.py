#!/usr/bin/python
# coding=utf-8

## time-spent: 1
import re
import sys
import reality
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

soup = BeautifulSoup(sys.stdin, 'html.parser')

info = {}

info["title"] = soup.find('h1').string.strip()
info["agency"] = soup.find('div', class_='brokerContacts').find('a').string.strip()
info["agency_person"] = soup.find_all('div', class_='brokerContacts')[1].find('p').string.strip()
info["text"] = soup.find('p', class_='popis')

for item in soup.find('div', id='params').find_all('p', {'class':['paramNo0', 'paramNo1']}):
    prop = item.find('span').string.strip()

    if prop == 'Lokalita:':
        info["street"] = item.find('strong', class_='street').string.strip()
    
        info["city"] = item.find('strong', class_='location').contents[1][2:]
        info["district"] =  item.find('span', class_='left150').string[6:]
    else:
        info[prop] = item.find('strong').string.strip()

    if prop == 'Cena:':
        info[prop] = re.sub(r"\s+", "", info[prop], flags=re.UNICODE)[:-1]
    elif prop == u'Úžitková plocha:':
        info[prop] = info[prop][:-3]

reality.printAdv([info], 'text')

