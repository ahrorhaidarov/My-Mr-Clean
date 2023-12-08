import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import re


def get_content(article_name):
    '''Send request to wikipedia about special title'''
    req = requests.get(f'https://en.wikipedia.org/wiki/{article_name}')
    soup = BeautifulSoup(req.content, 'html.parser')
    data = soup.find(id='bodyContent').find_all('p')
    return data


def merge_contents(data):
    '''Get the texts in one variable'''
    response = ''
    for line in data:
        response += line.text
    return response


def tokenize(content):
    '''Remove special element from the text'''
    return re.sub("[\(\[].*?[\)\]\)]", '', content).replace(',', '').replace('-', '').replace('  ', '').replace('.', '').replace(
        '\n', '').split(' ')


def lower_collection(collection):
    '''Turn all words to lowercase'''
    return [i.lower() for i in collection if i.isalpha()]


def count_frequency(collection):
    '''Create a dictionary and add keys as words and values as count of words in the text'''
    data_dict = {}
    for word in collection:
        data_dict[word] = collection.count(word)
    return data_dict


def print_most_frequent(frequencies, n):
    '''Print to concole most common words in specified size'''
    sorted_list = sorted([i for i in frequencies.values()], reverse=True)
    data_dict = {}
    for i in sorted_list:
        if n > 0:
            for key in frequencies.keys():
                if frequencies[key] == i:
                    data_dict[key] = i
        n -= 1
    return data_dict


def remove_stop_words(words, stop_words):
    '''Removing words from the specified stop_words'''
    words_copy = words.copy()
    for key in words_copy.keys():
        if key in stop_words:
            words.pop(key)
    return words


def barh(data):
    '''Print the barh chart'''
    x = [x for x in data.keys()]
    y = [y for y in data.values()]

    # Hexadecimal color codes
    hex_colors = [
        '#f891a2', '#f6928e', '#f29069', '#e2913d', '#ce9839',
        '#bd9c36', '#ad9e34', '#9da131', '#8ca632', '#72ab32',
        '#3db133', '#00b462', '#00b180', '#00b08f', '#00af9b',
        '#00aea5', '#00aeae', '#0fadb9', '#18aec6', '#27aed5',
        '#58afe7', '#8eaeed', '#aeaaf0', '#c4a1ef', '#d897ee',
        '#ed88ec', '#f684e0', '#f788cf', '#f68bc1', '#f78eb3'
    ]

    # Convert hexadecimal to RGB tuples
    rgb_colors = [tuple(int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)) for hex_color in hex_colors]

    plt.barh(x[::-1], y[::-1], height=0.5, color=rgb_colors)
    plt.title('Most common 20 words in the article')
    plt.show()


data = get_content('Ozone_layer')
merge_content = merge_contents(data)
collection = tokenize(merge_content)
collected = lower_collection(collection)
stop_words = ['the', 'layer', 'ozone', 'of', 'and', 'in', 'to', 'is', 'a', 'an',
              'by', 'that', 'for', 'was', 'were', 'are', 'from',
              'at', 'it', 'as', 'be', 'these', 'on', 'with', 'this',
              'have', 'has', 'other', 'because', 'can', 'its', 'out', 'about',
              'into', 'or', 'over', 'all', 'most', 'which', 'less', 'while', 'above', 'than', 's', 'a', 'b']
frequencies = count_frequency(collected)
filtered_collection = remove_stop_words(frequencies, stop_words)

most = print_most_frequent(filtered_collection, 20)
barh(most)