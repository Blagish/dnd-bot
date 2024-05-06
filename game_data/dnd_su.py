from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import quote
from discord import Embed, Colour
from cool_embed_tables import TableParser
import logging

logger = logging.getLogger(__name__)

blacklisted_tags = ['translate-by']
COLOUR = 0xfe650c
tags_with_new_strings = ('p', 'li', 'h1', 'h2', 'h3')


def parse_content(element, ignore_br=True):
    if isinstance(element, str):
        return element
    if not ignore_br and element.name == 'br':
        return ' '
    if element.text == '':
        return ''
    if element.attrs.get('class') and 'additionalInfo' in element.attrs.get('class'):
        return ''
    if element.name == 'table':
        table = TableParser(element, parse_string=parse_content, align_left='l', style='ms')
        return table.get_for_embed()

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
    logger.debug(f'dnd ru: looking for {name}')

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
        logger.debug('no results')
        return Embed(title="OwO, what's this?",
                     description='(по вашему запросу ничего не найдено)',
                     colour=Colour.red())

    for tag in results[:2]:
        title = tag.get_text()
        logger.debug(f'title is {title}')
        parts = title.split(' [')
        title = parts[1]
        if 'а' <= name[0] <= 'я':
            title = parts[0]
        if len(title) - len(name) < diff:
            diff = len(title) - len(name)
            possible_result = tag

    if possible_result is None:
        logger.debug('no results')
        return Embed(title="OwO, what's this?",
                     description='(по вашему запросу ничего не найдено)',
                     colour=Colour.red())
    target_url = base_url + possible_result.a.get('href')
    page = urlopen(target_url)
    soup = BeautifulSoup(page, 'html.parser')
    card = soup.find('div', attrs={'class': 'card__body', 'itemprop': 'articleBody'})
    title = possible_result.get_text()
    content = parse_content(card)
    content = content.replace('\n\n\n\n', '\n\n').replace('\n\n\n', '\n\n')
    embed_card = Embed(title=title,
                       url=target_url,
                       description=content,
                       colour=COLOUR)
    logger.debug('result found')
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
    print(get_spell('озорство').description)
