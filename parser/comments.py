from random import choice
import string
import re

letters = string.ascii_lowercase


def random_word(l=6):
    return ''.join(choice(letters) for i in range(l))


def replace(raw_string):
    dict_ = dict()
    comments = re.findall(r'([a-zA-Zа-яА-ЯёЁ][a-zA-Zа-яА-ЯёЁ_\s]+)[^\d(]', raw_string)  # it cuts off the last symbol of last words but still works so not my problem
    comments = list(set(comments))
    comments.sort(key=len, reverse=True)
    for comment in comments:
        hash_ = random_word()
        raw_string = raw_string.replace(comment, hash_)
        dict_[hash_] = comment
    return dict_, raw_string


def replace_back(dict_, raw_string):
    keys = list(dict_.keys())
    keys.sort(key=len, reverse=True)
    for h in keys:
        raw_string = raw_string.replace(h, dict_[h])
    return raw_string
