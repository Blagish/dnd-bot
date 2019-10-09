from bs4 import BeautifulSoup
import pandas as pd
import urllib
import re
import time

def get_spell(name): 
    def check_title(tag):
        return tag.has_attr('title') and name.lower() in tag.get('title').lower()

    base_url = "https://dungeon.su/"
    spells_url = "https://dungeon.su/spells/"
    page = urllib.request.urlopen(spells_url)
    soup = BeautifulSoup(page, 'html.parser')
    blacklisted_tags = ['translate-by']

    name = name.lower()
    print(name)
    
    b = soup.find(check_title)
    if b is None:
        print('owo wats this')
        return 'owo wats this'

    page = urllib.request.urlopen(base_url + b.get('href'))
    soup = BeautifulSoup(page, 'html.parser')
    card = soup.find('div', attrs={'class':'card-body'})   
    result = []
    result.append(soup.find('a', attrs={'class':'item-link'}).get_text())
    result.append('')
    for li in card.ul.contents:
        if (li.get('class') in blacklisted_tags) :
            continue
        if (li.get('class') == ['subsection', 'desc']):
            result.append('Описание:');
            li = li.div
        s = li.get_text()
        result.append(s)
    
    return '\n'.join(result)

    

#print(get_spell('Огонь фей'))

''
