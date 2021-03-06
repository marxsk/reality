#!/usr/bin/python
# coding=utf-8

## time-spent: 2+1+1+0.5+3
import re
import sys
import reality
import unicodedata
import lxml
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

soup = BeautifulSoup(sys.stdin, 'lxml')
results = []

for ad in soup.find_all('div', class_="inzerat"):
    info = {}

    info["title"] = ad.find('h2').find('a').string.strip()
    info["url"] = ad.find('h2').find('a')['href']
    info["offer"] = "predaj"

    info["update_date"] = ad.find_all('p', class_='grey')[1].find('span').string.strip()
    # @note: 1.1.17 -> 1.1.2017
    info["update_date"] = re.sub('(..)$', '20\\1', info["update_date"])

    if ad.find('span', class_='tlste red'):
        price_raw = ad.find('span', class_='tlste red').string

        if "/mes" in price_raw:
            info["offer"] = u"prenájom"
        price_raw = price_raw.replace('/mes.', '')
        price_raw = re.sub(r"\s+", "", price_raw, flags=re.UNICODE)
        price_raw = price_raw.strip()[:-1]
        info["price"] = float(price_raw)
    else:
        # @todo: log, catch 'dohodou'
        info["price"] = '#missing?'

    location_raw = ad.find('div', class_="locationText").contents[2].strip()
    if not "," in location_raw:
        info["location_city"] = location_raw
    else:
        (info["location_street"], info["location_city"]) = location_raw.split(",", 1)

    info["location_district"] = ad.find('div', class_="locationText").contents[3].string[1:-1].strip()

    if ad.find('p', class_='advertisement-condition'):
        info["condition"] = ad.find('p', class_='advertisement-condition').string.strip()

    raw_category = ad.find('a', class_='location').string.strip()
    raw_category_words = raw_category.split(' ')

    if (len(raw_category_words) > 3) and ('byt' == raw_category_words[2]):
        info["rooms"] = raw_category_words[0]
        info["category"] = "byt"

    if (len(raw_category_words) > 3):
        if ('dom' == raw_category_words[1]):
            info["category"] = "dom"
        elif ('pozemok' in raw_category_words):
            info["category"] = "pozemok"
        elif ('Pozemok' in raw_category_words):
            info["category"] = "pozemok"
        elif (u'Záhrada' in raw_category_words):
            info["category"] = u"záhrada"

    if (ad.find('p', class_='estate-area') and ad.find('p', class_='estate-area').find('span')):
        area_size_raw = ad.find('p', class_='estate-area').find('span').string
        content = ad.find('p', class_='estate-area').contents
        for x in range(1, len(content), 2):
            content[x+1] = re.sub(r"[.,]", "", content[x+1]).strip()
            content[x+1] = (''.join((c for c in unicodedata.normalize('NFD', content[x+1]) if unicodedata.category(c) != 'Mn')))

        info['size_' + content[x+1]] = float(re.sub(r"\s+", "", content[x].string, flags=re.UNICODE)[:-2])

    reality.renameKey(info, 'size_uzit', 'area_usable')
    reality.renameKey(info, 'size_pozemok', 'area_estate')
    reality.renameKey(info, 'size_zastav', 'area_built')

    results.append(info)
    # @todo: dom> izby, (chalupa?)
    # @todo: pozemok> inzinierske siete; pridaj typy (zahrada)
    # @todo: byt> poschodie, vytah, balkon, ...

    # @todo: realitka? - jednoducho sa da vytiahnut logo -> URL na web

if len(sys.argv) > 1 and sys.argv[1] == 'csv':
    reality.printAdv(results, 'csv')
else:
    reality.printAdv(results, None)
