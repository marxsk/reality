#!/usr/bin/python
# coding=utf-8

## time-spent: 1.5

from bs4 import BeautifulSoup
import unicodedata
import re
from pprint import pprint

with open('topreality') as fh:
    soup = BeautifulSoup(fh, 'html.parser')

    for ad in soup.find_all('div', class_="estate"):
        info = {}

        info["title"] = ad.find('h2').find('a').string.strip()
        info["url"] = ad.find('h2').find('a')['href']
        info["agency"] = ad.find('ul').find_all('li')[2].string
        info["condition"] = '#missing?' 

        raw_category = ad.find('ul').find_all('li')[0].string
        raw_category_words = raw_category.split(' ')
        info["offer"] = raw_category_words[-1]

        if (len(raw_category_words) > 3) and ('byt' == raw_category_words[2]):
            info["rooms"] = raw_category_words[0]
            info["type"] = "byt"

        if (len(raw_category_words) > 3):
            if ('dom' == raw_category_words[1]):
                info["type"] = "dom"
            elif ('pozemok' in raw_category_words):
                info["type"] = "pozemok"
            elif ('Pozemok' in raw_category_words):
                info["type"] = "pozemok"
            elif (u'Záhrada' in raw_category_words):
                info["type"] = u"záhrada"

        price_raw = ad.find('span', class_='price').find('strong').string
        price_raw = re.sub(r"\s+", "", price_raw, flags=re.UNICODE)
        price_raw = price_raw.strip()[:-1]
        info["price"] = float(price_raw.replace(',', '.'))

        location_raw = ad.find('span', class_='locality').string.strip()
        if not " , " in location_raw:
            info["location_city"] = location_raw
        else:
            (info["location_street"], info["location_city"]) = location_raw.split(" , ")

        #info["location_district"] => je v zátvorke v location_raw

        if ad.find('span', class_='areas'):
            content = ad.find('span', class_='areas').contents

            for x in range(0, len(content), 2):
                name = (content[x].replace(',', '').strip())
                value = (content[x+1].contents[0][:-1].strip())
                value = re.sub(r"\s+", "", value, flags=re.UNICODE)
                info['size_' + name] = float(value)

        pprint (info)