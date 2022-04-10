from bs4 import BeautifulSoup
from urllib.request import urlopen

blacklisted_tags = ['translate-by']


def get_spell(name):
    print('found spell', name)
    base_url = "https://dnd.su/"
    spells_url = "https://dnd.su/spells/"
    page = urlopen(spells_url)
    soup = BeautifulSoup(page, 'html.parser')

    name = name.lower()
    results = soup.find_all(lambda x: x.has_attr('title') and name.lower() in x.get('title').lower())

    possible_result = None
    diff = 1e9

    if len(results) == 0:
        print('owo wats this')
        return 'owo wats this'

    for tag in results:
        title = tag.get('title').lower()
        print('title is ' + title)
        parts = title.split(' [')
        title = parts[1]
        if 'а' <= name[0] <= 'я':
            title = parts[0]
        if len(title) - len(name) < diff:
            diff = len(title) - len(name)
            possible_result = tag

    if possible_result is None:
        print('owo wats this')
        return 'owo wats this'

    page = urlopen(base_url + possible_result.get('href'))
    soup = BeautifulSoup(page, 'html.parser')
    card = soup.find('div', attrs={'class': 'card-body'})
    result = [soup.find('a', attrs={'class': 'item-link'}).get_text(), '']
    for li in card.ul.contents:
        if li.get('class') in blacklisted_tags:
            continue
        if li.get('class') == ['subsection', 'desc']:
            result.append('**Описание:**')
            li = li.div
        s = li.get_text()
        result.append(s)

    return '\n'.join(result)



