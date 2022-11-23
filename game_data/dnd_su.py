from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import quote
from discord import Embed, Colour
from prettytable import PrettyTable

blacklisted_tags = ['translate-by']
COLOUR = 0xfe650c
tags_with_new_strings = ('p', 'li', 'h1', 'h2', 'h3')


def parse_table(table):
    table = table.tbody  # hop to tbody
    data = table.children
    next(data)
    header = next(data)
    headers = []
    for h in header.children:
        if h != '\n':
            headers.append(parse_content(h, ignore_br=False))
    print(headers)
    t = PrettyTable(headers)
    for child in data:
        if child == '\n':
            continue
        a = []
        for c in child.children:
            if c != '\n':
                a.append(parse_content(c, ignore_br=False))
        t.add_row(a)
    return str(t)


def parse_content(element, ignore_br=True):
    if isinstance(element, str):
        return element
    if not ignore_br and element.name == 'br' :
        return ' '
    if element.text == '':
        return ''
    if element.attrs.get('class') and 'additionalInfo' in element.attrs.get('class'):
        return ''
    if element.name == 'table':
        return parse_table(element)

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
        text += parse_content(child, ignore_br=ignore_br)
    return f'{style1}{text}{style2}'


def get_spell(name):
    print('dnd ru: looking for', name)

    if len(name) < 4:
        return Embed(title="You baka!",
                     description='(поисковой запрос должен быть больше трех символов)',
                     colour=Colour.red())

    base_url = "https://dnd.su/"
    spells_url = "https://dnd.su/spells/?search="
    name = '+'.join(name.lower().split())
    page = urlopen(spells_url+quote(name, safe='+'))
    soup = BeautifulSoup(page, 'html.parser')
    results = soup.find_all('h2', attrs={'class': 'card-title'})
    possible_result = None
    diff = 1e9

    if results[0].get_text().startswith('По вашему'):
        return Embed(title="OwO, what's this?",
                     description='(по вашему запросу ничего не найдено)',
                     colour=Colour.red())

    for tag in results:
        title = tag.get_text()
        print('title is ' + title)
        parts = title.split(' [')
        title = parts[1]
        if 'а' <= name[0] <= 'я':
            title = parts[0]
        if name not in title.lower():
            print('not ' + title)
            continue
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
    content = parse_content(card)
    content = content.replace('\n\n\n\n', '\n\n').replace('\n\n\n', '\n\n')
    embed_card = Embed(title=title,
                       url=target_url,
                       description=content,
                       colour=COLOUR)
    return embed_card


def get_english_name(name):
    spells_url = "https://dnd.su/spells/?search="
    name = '+'.join(name.lower().split())
    page = urlopen(spells_url+quote(name, safe='+'))
    soup = BeautifulSoup(page, 'html.parser')
    results = soup.find_all('h2', attrs={'class': 'card-title'})
    possible_result = None
    diff = 1e9
    if results[0].get_text().startswith('По вашему'):
        return None
    for tag in results:
        title = tag.get_text()
        parts = title.split(' [')
        title = parts[0]
        if len(title) - len(name) < diff:
            diff = len(title) - len(name)
            possible_result = parts[1][:-1]
    return possible_result


if __name__ == '__main__':
    print(get_spell('телепортация').description)
