from bs4 import BeautifulSoup
from urllib.request import Request
from urllib.request import urlopen
import csv
import re

csv_data = {}
with open('RadGridExport.csv') as pf2_data: # на будущее: при обновлении бд заменять буквы в deja vu на нормальные
    next(pf2_data)
    reader = csv.reader(pf2_data)
    for rows in reader:
        print(rows[0])
        link, name = re.findall(r'href="(Spells.aspx\?ID=\d+)">([\w\s\'\-,]+)<', rows[0])[0]
        print(link, name)
        csv_data[name.lower()] = link


def get_info(name):
    def check_title(name_from_db):
        if name in name_from_db or name in name_from_db.replace("'", '') or name in name_from_db.replace(",", ''):
            return True

    base_url = 'https://2e.aonprd.com/'
    results = list(filter(check_title, csv_data.keys()))
    diff = 1e9
    if len(results) == 0:
        print('owo wats this')
        return 'owo wats this'

    possible_result = None
    for poss_result in results:
        if len(poss_result) - len(name) < diff:
            diff = len(poss_result) - len(name)
            possible_result = poss_result

    if possible_result is None:
        print('owo wats this')
        return 'owo wats this'

    url = base_url + csv_data[possible_result]
    page = urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')


#     url = base_url + b.get('href')
#     print(url)
#     page = urllib.request.urlopen(url)
#
#     soup = BeautifulSoup(page, 'html.parser')
#     card = soup.find('span', attrs={'id': 'ctl00_MainContent_DetailedOutput'})
#     return soup
#     result = [soup.find('a', attrs={'class': 'item-link'}).get_text(), '']
#     for li in card.ul.contents:
#         if li.get('class') in blacklisted_tags:
#             continue
#         if li.get('class') == ['subsection', 'desc']:
#             result.append('Описание:')
#             li = li.div
#         s = li.get_text()
#         result.append(s)
#     return '\n'.join(result)