import nltk
from bs4 import BeautifulSoup
from os import walk
import pymorphy2

invalid_poses = ['CONJ', 'PREP']
cleaned_tokens = []

morph = pymorphy2.MorphAnalyzer()

# getting tokens
filenames = next(walk('Pages'), (None, None, []))[2]
for filename in filenames:
    with open('Pages/'+filename, mode='r', encoding='utf-8') as file:
        data = file.read()
        soup = BeautifulSoup(data, features='html.parser')
        page_tokens = nltk.word_tokenize(' '.join(soup.find('div', {'class': 'post-inner'}).stripped_strings).lower())
        for token in page_tokens:
            if not any([letter.isdigit() for letter in token]) or r'//' in token:
                parsed_token = morph.parse(token)[0]
                if parsed_token.tag.POS and parsed_token.tag.POS not in invalid_poses:
                    cleaned_tokens.append(token)

tokens_set = set(cleaned_tokens)

# writing tokens
with open('tokens.txt', mode='w', encoding='utf-8') as tokens:
    for token in tokens_set:
        tokens.write(f'{token}\n')

# getting lemmas
lemma_mapping = dict()
for token in tokens_set:
    parsed_token = morph.parse(token)[0]
    token_lemma = parsed_token.normal_form
    if token_lemma not in lemma_mapping.keys():
        lemma_mapping[token_lemma] = [token]
    else:
        lemma_mapping[token_lemma].append(token)

# writing lemmas
with open('lemmas.txt', mode='w', encoding='utf-8') as lemmas:
    for key, values in lemma_mapping.items():
        lemmas.write(f'{key} {" ".join(values)}\n')
