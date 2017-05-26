#!/usr/bin/python
# coding=utf-8

## time-spent: 1.5
import re
import sys
import reality
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

soup = BeautifulSoup(sys.stdin, 'html.parser')
results = []

for ad in soup.find_all('div', class_="estate"):
    info = {}

    info["title"] = ad.find('h2').find('a').string.strip()
    info["url"] = ad.find('h2').find('a')['href']
    if (len(ad.find('ul').find_all('li')) > 2):
        info["agency"] = ad.find('ul').find_all('li')[2].string

    raw_category = ad.find('ul').find_all('li')[0].string
    raw_category_words = raw_category.split(' ')
    info["offer"] = raw_category_words[-1]

    if (len(raw_category_words) > 3) and ('byt' == raw_category_words[2]):
        info["rooms"] = raw_category_words[0]
        info["category"] = "byt"

    if len(raw_category_words) > 3:
        if 'dom' == raw_category_words[1]:
            info["category"] = "dom"
        elif 'pozemok' in raw_category_words:
            info["category"] = "pozemok"
        elif 'Pozemok' in raw_category_words:
            info["category"] = "pozemok"
        elif u'Záhrada' in raw_category_words:
            info["category"] = u"záhrada"

    if not ad.find('span', class_='price').find('strong'):
        price_raw = "#missing"
    else:
        price_raw = ad.find('span', class_='price').find('strong').string
        price_raw = re.sub(r"\s+", "", price_raw, flags=re.UNICODE)
        price_raw = price_raw.strip()[:-1]
        price_raw = price_raw.replace(',', '.')
        if "+" in price_raw:
            v = price_raw.split('+')
            info["price"] = float(v[0])
            info["price_energy"] = float(v[1])
        else:
            info["price"] = float(price_raw)

    location_raw = ad.find('span', class_='locality').string.strip()
    if " , " not in location_raw:
        info["location_city"] = location_raw
    else:
        (info["location_street"], info["location_city"]) = location_raw.split(" , ")

    #info["location_district"] => je v zátvorke v location_raw

    info["update_date"] = ad.find('span', class_='date').string

    if ad.find('span', class_='areas'):
        content = ad.find('span', class_='areas').contents

        for x in range(0, len(content), 2):
            name = (content[x].replace(',', '').strip())
            value = (content[x+1].contents[0][:-1].strip())
            value = re.sub(r"\s+", "", value, flags=re.UNICODE)
            info[u'size_' + name] = float(value)

    ## unification
    reality.renameKey(info, u'size_úžitková plocha', 'area_usable')
    reality.renameKey(info, u'size_pozemok', 'area_estate')
    reality.renameKey(info, u'size_zastavaná plocha', 'area_built')

    results.append(info)

if len(sys.argv) > 1 and sys.argv[1] == 'csv':
    reality.printAdv(results, 'csv')
else:
    reality.printAdv(results, None)
