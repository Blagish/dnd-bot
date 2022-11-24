from bs4 import BeautifulSoup
from urllib.request import urlopen
from discord import Embed, Colour
from cool_embed_tables import TableParser

blacklisted_tags = []
CARDS_COLORS = {'NORMAL': 0xc4af63,
                'UNEARTHED_ARCANA': 0x980082}
tags_with_new_strings = ('p', 'li', 'h1', 'h2', 'h3')

FOOTER_URL = 'https://cdn.discordapp.com/attachments/778998112819085352/964148715067670588/unknown.png'


def parse_content(element, ignore_br=True):
    if isinstance(element, str):
        return element
    if not ignore_br and element.name == 'br':
        return ' '
    if element.text == '':
        return ''
    if element.name == 'table':
        table = TableParser(element, parse_string=parse_content, align_left='l', style='ms')
        return table.get_for_embed()

    style1 = style2 = ''
    text = ''
    if element.name in tags_with_new_strings:
        style2 = '\n'
        if element.name == 'li' and element.attrs.get('class') != ['subsection', 'desc']:
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
    print('dnd en: looking for', name)

    if len(name) < 4:
        return Embed(title="You baka!",
                     description='(поисковой запрос должен быть больше трех символов)',
                     colour=Colour.red())

    base_url = "http://dnd5e.wikidot.com/"
    spells_url = "http://dnd5e.wikidot.com/spells"
    COLOUR = CARDS_COLORS['NORMAL']
    name = name.lower()
    page = urlopen(spells_url)
    soup = BeautifulSoup(page, 'html.parser')
    results = soup.find_all(lambda x: x and x.name == 'td' and x.a and name in x.get_text().lower())
    possible_result = None
    diff = 1e9

    if len(results) == 0:
        return Embed(title="OwO, what's this?",
                     description='(по вашему запросу ничего не найдено)',
                     colour=Colour.red())

    for tag in results:
        title = tag.get_text()
        print('title is ' + title)
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
    card = soup.find('div', attrs={'id': 'page-content'})
    ps = card.find_all('p')
    source = ps[0].get_text()
    source = source[source.find(' '):]
    content = parse_content(card)
    content = content.replace('**Casting Time', '> **Casting Time').replace('**Range', '> **Range').replace('**Components', '> **Components').replace('**Duration', '> **Duration')
    content = content[content.find('\n', 2):]
    content = '> ' + content.replace('\n', '', 3)
    content = content.replace('\n\n\n\n', '\n\n').replace('\n\n\n', '\n\n')
    title = soup.find('div', attrs={'class': 'page-title'}).get_text()
    if '(UA)' in title:
        COLOUR = CARDS_COLORS['UNEARTHED_ARCANA']
    embed_card = Embed(title=title,
                       url=target_url,
                       description=content,
                       colour=COLOUR)
    embed_card.set_footer(text=source, icon_url=FOOTER_URL)
    return embed_card


if __name__ == '__main__':
    print(get_spell('chaos bolt').description)
