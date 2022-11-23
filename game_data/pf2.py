import requests
from bs4 import BeautifulSoup
from discord import Embed, Colour
from prettytable import PrettyTable

tags_with_new_strings = ('p', 'li', 'h1', 'h2', 'h3')

ACTIONS = {'action1': ':one:',
           'action2': ':two:',
           'action3': ':three:',
           'actionF': ':free:',
           'Reaction': ':leftwards_arrow_with_hook:'}

CARDS_COLORS = {'EMPTY': 0x090a0a,
                'NORMAL': 0x7289da,
                'UNCOMMON': 0xff6e00,
                'RARE': 0x1522b2,
                'UNIQUE': 0xa600a6}

FOOTER_URL = 'https://cdn.discordapp.com/attachments/778998112819085352/964148715067670588/unknown.png'

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
        if len(a) == len(headers):
            t.add_row(a)
    return '`' + str(t) + '`'


def parse_content(element, ignore_br=True):
    if isinstance(element, str):
        return element
    if not ignore_br and element.name == 'br':
        return ' '
    if element.name == 'i':
        action_class = element.attrs['class'][1]
        return ACTIONS[action_class]
    if element.text == '':
        return ''
    if element.name == 'table':
        return parse_table(element)

    style1 = style2 = ''
    text = ''
    if element.name in tags_with_new_strings:
        style2 = '\n'
        if element.name == 'li':
            style1 = '- '
    elif element.attrs.get('data-toggle') is not None:
        style1 = style2 = '__'
    elif element.name == 'em':
        style1 = style2 = '*'
    elif element.name == 'strong':
        style1 = style2 = '**'
    for child in element.children:
        text += parse_content(child, ignore_br=ignore_br)
    return f'{style1}{text}{style2}'


def get_info(name):
    print('pf: looking for', name)
    search_url = 'https://pf2easy.com/php/search.php'
    thing_url = 'https://pf2easy.com/index.php'
    response = requests.post(search_url, {'name': name})
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('button')

    if len(results) == 0:
        return Embed(title="OwO, what's this?",
                     description='(по вашему запросу ничего не найдено)',
                     colour=Colour.red())

    ans = results[0]
    # if len(results) > 1:
    #     ans_type = ans.find('small').text
    #     ans_name = ans.find('strong').text
    #     if ans_name != name:
    #         ans_text += f'Нашла больше одного варианта ответа. Использую ближайший:{ans_type} под названием {ans_name}.\n\n'
    #     elif results[1].find('strong') == name:
    #         ans_text += f'Нашла больше одного варианта ответа с идентичным именем.\n\n'
    res_id = ans.find('input').attrs['value']
    data = requests.get(thing_url + f'?id={res_id}')
    soup = BeautifulSoup(data.text, 'html.parser')

    title = soup.find_all('h1')[-1].text.title()
    level = soup.find('h2').text.replace('×', '').replace('\n', '').lower()  # not only a level, but feat type, etc.
    description = f'*{level}*\n'
    color = CARDS_COLORS['EMPTY']
    source = soup.find('div', attrs={'class': 'source'}).text

    if (traits := soup.find('section', attrs={'class': 'traits'})) is not None:
        traits_text = traits.get_text('|').split('|')
        color = CARDS_COLORS.get(traits_text[0], CARDS_COLORS['NORMAL'])
        description += '> **Traits** `' + '`, `'.join(traits_text) + '`\n'

    addon = False
    if (details := soup.find('section', attrs={'class': 'details'})) is not None:
        if 'addon' not in details.attrs['class']:
            details_text = '> ' + parse_content(details).replace('\n**', '\n> **')
            description += details_text
        else:
            addon = True  # добавить потом типа таблицы в общем да как в архетипах.

    if (content := soup.find('section', attrs={'class': 'content'})) is not None:
        description += parse_content(content)

    if len(contents_extra := soup.find_all('section', attrs={'class': ['content extra']})) > 0:
        for content_extra in contents_extra:
            description += parse_content(content_extra)
            # embed_card.add_field(name='', value=parse_content(content_extra), inline=False)

    embed_card = Embed(title=title, description=description, color=color)
    embed_card.set_footer(text=source, icon_url=FOOTER_URL)

    return embed_card


if __name__ == '__main__':
    print(get_info('chromatic wall'))
