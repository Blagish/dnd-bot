import requests
import re
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
        ans_text += f'Нашла больше одного варианта ответа. Использую ближайший:{ans_type} под названием {ans_name}.\n\n'
    res_id = ans.find('input').attrs['value']
    data = requests.get(thing_url + f'?id={res_id}')
    soup = BeautifulSoup(data.text, 'html.parser')
    name = soup.find_all('h1')[-1].text
    level = soup.find('h2').text
    ans_text += f'{name}; {level}\n'
    traits = soup.find('section', attrs={'class': 'traits'})
    if traits is not None:
        traits_text = traits.get_text('|').split('|')
        ans_text += 'Traits: [' + '], ['.join(traits_text) + ']\n'

    details = soup.find('section', attrs={'class': 'details'})
    addon = False
    if details is not None:
        if 'addon' not in details.attrs['class']:
            all_details = details.find_all('p')
            for d in all_details:
                text = d.text
                if 'Cast' in text:
                    action = soup.find('i', attrs={'class': 'pf2'}).attrs['title']
                    strings = [i for i in d.strings]
                    strings[2] = f'{action}: '
                    text = ''.join(strings)
                ans_text += text + '\n'
        else:
            addon = True # добавить потом типа таблицы в общем да как в архетипах.
    content = soup.find_all('section', attrs={'class': 'content'})
    for c in content:
        ans_text += c.text + '\n\n'

    return ans_text
