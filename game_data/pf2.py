import requests
from bs4 import BeautifulSoup


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
        ans_text += content.text + '\n\n'

    if (content_extra := soup.find('section', attrs={'class': ['content', 'extra']})) is not None:
        ans_text += content_extra.text + '\n\n'

    # content extra
    return ans_text
