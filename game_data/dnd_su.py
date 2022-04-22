from bs4 import BeautifulSoup
from urllib.request import urlopen
from discord import Embed

blacklisted_tags = ['translate-by']


def get_spell(name):
    print('dnd: looking for', name)
    base_url = "https://dnd.su/"
    spells_url = "https://dnd.su/spells/"
    page = urlopen(spells_url)
    soup = BeautifulSoup(page, 'html.parser')

    name = name.lower()
    results = soup.find_all(lambda x: x.has_attr('title') and name.lower() in x.get('title').lower())

    possible_result = None
    diff = 1e9

    if len(results) == 0:
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
        return 'owo wats this'

    target_url = base_url + possible_result.get('href')
    page = urlopen(target_url)
    soup = BeautifulSoup(page, 'html.parser')
    card = soup.find('div', attrs={'class': 'card-body'})
    result = [soup.find('a', attrs={'class': 'item-link'}).get_text(), '']
    title = soup.find('a', attrs={'class': 'item-link'}).get_text()
    desc = soup.find('li', class_="size-type-alignment").get_text()
    print(desc)
    embed = Embed(title=title, url=target_url, description=desc)
    #fields = ['уровень', 'время', "дистанция", "компоненты", "длительность", "классы", "ахетипы", "источник"]
    for li in card.ul.contents:
        raw = str(li)
        if '<strong>' in raw:
# get text inside strong tag, strip off the semicolon so the inline looks nicer
            title = raw.split('<strong>')[1].split('</strong>')[0][:-1]
            print(f'field title is {title}') 
            desc = raw.split('</strong>')[1]
            embed.add_field(name=title, value=desc, inline=True)
        if li.get('class') in blacklisted_tags:
            continue
        if li.get('class') == ['subsection', 'desc']:
            result.append('**Описание:**')
            li = li.div
        s = str(li)
        result.append(s)
    
    desc = soup.find('li', class_="subsection desc").div.get_text()
    print('desc is ' + desc)
    embed.add_field(name='Описание', value=desc, inline=False)
    #return '\n'.join(result)
    return embed

if __name__ == '__main__':
    print(get_spell('fireball'))
