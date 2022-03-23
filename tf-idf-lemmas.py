import nltk
from bs4 import BeautifulSoup
from os import walk
import pymorphy2
import math

invalid_poses = ['CONJ', 'PREP']
morph = pymorphy2.MorphAnalyzer()
inverted_index = dict()
with open('inverted_index_by_lemmas.txt', encoding='utf-8') as input_file:
    lines = input_file.readlines()
    for line in lines:
        key = line.rstrip().split(' ')[0]
        values = line.rstrip().split(' ')[1:]
        inverted_index[key] = values


filenames = next(walk('Pages'), (None, None, []))[2]
N = len(filenames)
for filename in filenames:
    cleaned_tokens = []
    cleaned_lemmas_amount = dict()
    with open('Pages/'+filename, mode='r', encoding='utf-8') as file:
        data = file.read()
        soup = BeautifulSoup(data, features='html.parser')
        page_tokens = nltk.word_tokenize(' '.join(soup.find('div', {'class': 'post-inner'}).stripped_strings).lower())
        for token in page_tokens:
            if not any([letter.isdigit() for letter in token]) or r'//' in token:
                parsed_token = morph.parse(token)[0]
                if parsed_token.tag.POS and parsed_token.tag.POS not in invalid_poses:
                    token_lemma = parsed_token.normal_form
                    if token_lemma not in cleaned_lemmas_amount.keys():
                        cleaned_lemmas_amount[token_lemma] = 1
                    else:
                        cleaned_lemmas_amount[token_lemma] += 1
                    cleaned_tokens.append(token)
    tokens_set = set(cleaned_tokens)
    with open(f'Lemmas-tf-idf/tf-lemmas-{filename}', mode='w', encoding='utf-8') as output:
        for lemma in cleaned_lemmas_amount.keys():
            Nw = len(inverted_index[lemma])
            tf = cleaned_lemmas_amount[lemma]
            idf = math.log(Nw/N)
            tf_idf = tf * idf
            output.write(f'{lemma} {idf} {tf_idf}\n')
