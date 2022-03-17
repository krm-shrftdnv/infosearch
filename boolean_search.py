inverted_index = dict()

AND_OPERATOR = 'AND'
OR_OPERATOR = 'OR'

with open('inverted_index.txt', encoding='utf-8') as input_file:
    lines = input_file.readlines()
    for line in lines:
        key = line.rstrip().split(' ')[0]
        values = line.rstrip().split(' ')[1:]
        inverted_index[key] = values


def or_operation(query_words):
    result = []
    for token in query_words:
        if inverted_index[token]:
            result.extend(inverted_index[token])
    return set(result)


def and_operator(query_words):
    pages = []
    for token in query_words:
        if inverted_index[token]:
            pages.append(set(inverted_index[token]))
    result = pages[0]
    for page in pages:
        result &= page
    return result


def search(operator, query_words):
    if operator == OR_OPERATOR:
        return or_operation(query_words)
    elif operator == AND_OPERATOR:
        return and_operator(query_words)


if __name__ == '__main__':
    query = input('Введите запрос:\n')
    args = query.split(' ')
    if len(args) > 1:
        operator = args[0].upper()
    else:
        operator = OR_OPERATOR

    print(search(operator, args[1:]))
