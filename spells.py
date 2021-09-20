from bs4 import BeautifulSoup
# import pandas as pd
import urllib
# import re
# import time


def get_spell_dungeon_su(name):
    def check_title(tag):
        return tag.has_attr('title') and name.lower() in tag.get('title').lower()
    print('found spell', name)
    base_url = "https://dungeon.su/"
    spells_url = "https://dungeon.su/spells/"
    page = urllib.request.urlopen(spells_url)
    soup = BeautifulSoup(page, 'html.parser')
    blacklisted_tags = ['translate-by']

    name = name.lower()
    print(name)

    results = soup.find_all(check_title)
    diff = 1e9
    b = None
    for tag in results:
        title = tag.get('title').lower()
        print('title is ' + title)
        parts = title.split(' [')
        if name[0] in 'йцукенгшщзхъфывапролджэячсмитьбю':
            title = parts[0]
        else:
            title = parts[1]
        if len(title) - len(name) < diff:
            diff = len(title) - len(name)
            b = tag

    if b is None:
        print('owo wats this')
        return 'owo wats this'

    page = urllib.request.urlopen(base_url + b.get('href'))
    soup = BeautifulSoup(page, 'html.parser')
    card = soup.find('div', attrs={'class': 'card-body'})
    result = [soup.find('a', attrs={'class': 'item-link'}).get_text(), '']
    for li in card.ul.contents:
        if li.get('class') in blacklisted_tags:
            continue
        if li.get('class') == ['subsection', 'desc']:
            result.append('Описание:')
            li = li.div
        s = li.get_text()
        result.append(s)

    return '\n'.join(result)


def get_spell_aon(name):
    def check_title(tag):
        return tag.has_attr('href') and name.lower() in tag.get_text().lower()
    print('found spell', name)
    base_url = 'https://2e.aonprd.com/'
    spells_url = 'https://2e.aonprd.com/SpellLists.aspx?Tradition=0'
    page = urllib.request.urlopen(spells_url)
    soup = BeautifulSoup(page, 'html.parser')
    name = name.lower()

    results = soup.find_all(check_title)
    diff = 1e9
    b = None
    for tag in results:
        title = tag.get_text().lower()[:-6]
        print('title is ' + title)
        if len(title) - len(name) < diff:
            diff = len(title) - len(name)
            b = tag

    if b is None:
        print('owo wats this')
        return 'owo wats this'
    url = base_url + b.get('href')
    print(url)
    page = urllib.request.urlopen(url)

    soup = BeautifulSoup(page, 'html.parser')
    card = soup.find('span', attrs={'id': 'ctl00_MainContent_DetailedOutput'})
    return soup
    result = [soup.find('a', attrs={'class': 'item-link'}).get_text(), '']
    for li in card.ul.contents:
        if li.get('class') in blacklisted_tags:
            continue
        if li.get('class') == ['subsection', 'desc']:
            result.append('Описание:')
            li = li.div
        s = li.get_text()
        result.append(s)
    return '\n'.join(result)
