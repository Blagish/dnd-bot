import requests
from bs4 import BeautifulSoup

tags_with_new_strings = ('p', 'li', 'h1', 'h2', 'h3')

ACTIONS = {'action1': ':one:',
           'action2': ':two:',
           'action3': ':three:',
           'actionF': ':free:',
           'Reaction': ':leftwards_arrow_with_hook:'}


def parse_content(element):
    if isinstance(element, str):
        return element
    if element.name == 'i':
        action_class = element.attrs['class'][1]
        return ACTIONS[action_class]
    if element.text == '':
        return ''

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
        text += parse_content(child)
    return f'{style1}{text}{style2}'


def get_info(name):
    search_url = 'https://pf2easy.com/php/search.php'
    thing_url = 'https://pf2easy.com/index.php'
    response = requests.post(search_url, {'name': name})
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('button')

    if len(results) == 0:
        print('owo wats this')
        return 'owo wats this'

    ans_text = ''
    ans = results[0]
    if len(results) > 1:
        ans_type = ans.find('small').text
        ans_name = ans.find('strong').text
        if ans_name != name:
            ans_text += f'Нашла больше одного варианта ответа. Использую ближайший:{ans_type} под названием {ans_name}.\n\n'
        elif results[1].find('strong') == name:
            ans_text += f'Нашла больше одного варианта ответа с идентичным именем.\n\n'
    res_id = ans.find('input').attrs['value']
    data = requests.get(thing_url + f'?id={res_id}')
    soup = BeautifulSoup(data.text, 'html.parser')

    name = soup.find_all('h1')[-1].text.title()
    level = soup.find('h2').text.replace('×', '').replace('\n', '').lower()
    ans_text += f'**{name}** *({level})*\n'

    if (traits := soup.find('section', attrs={'class': 'traits'})) is not None:
        traits_text = traits.get_text('|').split('|')
        ans_text += '> **Traits** [' + '], ['.join(traits_text) + ']\n'

    addon = False
    if (details := soup.find('section', attrs={'class': 'details'})) is not None:
        if 'addon' not in details.attrs['class']:
            details_text = '> ' + parse_content(details).replace('\n**', '\n> **')
            ans_text += details_text
        else:
            addon = True # добавить потом типа таблицы в общем да как в архетипах.

    if (content := soup.find('section', attrs={'class': 'content'})) is not None:
        ans_text += parse_content(content)+'\n'

    if len(contents_extra := soup.find_all('section', attrs={'class': ['content extra']})) > 0:
        for content_extra in contents_extra:
            ans_text += parse_content(content_extra)+'\n'

    return ans_text


if __name__ == '__main__':
    print(get_info('chromatic wall'))
