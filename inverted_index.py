from os import walk

import nltk
import pymorphy2
from bs4 import BeautifulSoup

invalid_poses = ['CONJ', 'PREP']
inverted_index = dict()

morph = pymorphy2.MorphAnalyzer()


def update_inverted_index(index_map, array, value):
    for elem in array:
        if elem not in index_map.keys():
            index_map[elem] = [value]
        else:
            index_map[elem].append(value)


# getting tokens
filenames = next(walk('../crawler/common/storage'), (None, None, []))[2]
for filename in filenames:
    with open('../crawler/common/storage/' + filename, mode='r', encoding='utf-8') as file:
        cleaned_tokens = []
        data = file.read()
        soup = BeautifulSoup(data, features='html.parser')
        page_tokens = nltk.word_tokenize(' '.join(soup.find('div', {'class': 'post-inner'}).stripped_strings).lower())
        for token in page_tokens:
            if not any([letter.isdigit() for letter in token]) or r'//' in token:
                parsed_token = morph.parse(token)[0]
                if parsed_token.tag.POS and parsed_token.tag.POS not in invalid_poses:
                    cleaned_tokens.append(token)
        cleaned_tokens = set(cleaned_tokens)
        value = filename.split('.')[0]
        update_inverted_index(inverted_index, cleaned_tokens, value)

# writing inverted index
with open('inverted_index.txt', mode='w', encoding='utf-8') as file:
    for key, values in inverted_index.items():
        file.write(f'{key} {" ".join(values)}\n')
