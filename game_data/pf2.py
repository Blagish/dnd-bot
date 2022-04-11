import requests
from bs4 import BeautifulSoup


def parse_content(element, text):
    if isinstance(element, str):
        text += element
        return text
    if element.text == '':
        return text
    if element.attrs.get('data-toggle') is not None:
        text += f'__{element.text}__'
        return text
    if element.name == 'em':
        text += f'*{element.text}*'
        return text
    if element.name == 'strong':
        text += f'**{element.text}**'
        return text

    if element.name == 'li':
        text += '\n- '
    for child in element.children:
        text = parse_content(child, text)
    return text


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
    ans_text += f'> **{name}** *({level})*\n'

    if (traits := soup.find('section', attrs={'class': 'traits'})) is not None:
        traits_text = traits.get_text('|').split('|')
        ans_text += '**Traits:** [' + '], ['.join(traits_text) + ']\n'

    addon = False
    if (details := soup.find('section', attrs={'class': 'details'})) is not None:
        if 'addon' not in details.attrs['class']:
            all_details = details.find_all('p')
            for d in all_details:
                text = [i for i in d.strings]
                if 'Cast' in text or 'Cast ' in text:
                    action = soup.find('i', attrs={'class': 'pf2'}).attrs['title']
                    text = [i for i in d.strings]
                    text[2] = f'*{action}*, '
                text[0] = f'**{text[0]}:**'
                ans_text += ''.join(text) + '\n'
        else:
            addon = True # добавить потом типа таблицы в общем да как в архетипах.

    if (content := soup.find('section', attrs={'class': 'content'})) is not None:
        ans_text += parse_content(content, '')+'\n\n'

    if len(contents_extra := soup.find_all('section', attrs={'class': ['content extra']})) > 0:
        for content_extra in contents_extra:
            ans_text += parse_content(content_extra, '')+'\n\n'

    return ans_text
