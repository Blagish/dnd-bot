from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import quote
from discord import Embed, Colour

blacklisted_tags = ['translate-by']
COLOUR = 0xfe650c
tags_with_new_strings = ('p', 'li', 'h1', 'h2', 'h3')


def parse_content(element):
    if isinstance(element, str):
        return element
    if element.text == '':
        return ''

    style1 = style2 = ''
    text = ''
    if element.name in tags_with_new_strings:
        style2 = '\n'
        if element.name == 'li' and element.attrs.get('class') == ['size-type-alignment']:
            style1 = '> *'
            style2 = '*\n'
        elif element.name == 'li' and element.attrs.get('class') != ['subsection', 'desc']:
            style1 = '> '

    elif element.attrs.get('class') == ['size-type-alignment']:
        style1 = style2 = '__'
    elif element.name == 'em':
        style1 = style2 = '*'
    elif element.name == 'strong':
        style1 = style2 = '**'
    for child in element.children:
        text += parse_content(child)
    return f'{style1}{text}{style2}'


def get_spell(name):
    print('dnd: looking for', name)
    base_url = "https://dnd.su/"
    spells_url = "https://dnd.su/spells/?search="
    name = '+'.join(name.lower().split())
    page = urlopen(spells_url+quote(name, safe='+'))
    soup = BeautifulSoup(page, 'html.parser')
    results = soup.find_all('h2', attrs={'class': 'card-title'})
    possible_result = None
    diff = 1e9

    if len(results) == 0:
        return 'owo wats this'

    for tag in results:
        title = tag.get_text()
        print('title is ' + title)
        parts = title.split(' [')
        title = parts[1]
        if 'а' <= name[0] <= 'я':
            title = parts[0]
        if len(title) - len(name) < diff:
            diff = len(title) - len(name)
            possible_result = tag

    if possible_result is None:
        return Embed(title="OwO, what's this?",
                     description='(по вашему запросу ничего не найдено)',
                     colour=Colour.red())
    target_url = base_url + possible_result.a.get('href')
    page = urlopen(target_url)
    soup = BeautifulSoup(page, 'html.parser')
    card = soup.find('div', attrs={'class': 'card-body', 'itemprop': 'articleBody'})
    title = possible_result.get_text()
    embed_card = Embed(title=title,
                       url=target_url,
                       description=parse_content(card),
                       colour=COLOUR)
    print(parse_content(card))
    return embed_card


if __name__ == '__main__':
    print(get_spell('fireball'))
