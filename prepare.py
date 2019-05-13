# Preparation
from acquire import get_all_readme_files_and_languages
import unicodedata
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import pandas as pd


def basic_clean(item):
    '''
    take in a string (item) and return it after applying some basic text cleaning to it:
        - lowercase everything
        - normalize unicode characters
        - replace anything that is not a letter, number, whitespace or a single quote
    '''
    new_item = item.lower()
    new_item = re.sub(r'\s', ' ', new_item)
    normalized = unicodedata.normalize('NFKD', new_item)                .encode(
        'ascii', 'ignore')                .decode('utf-8')
    without_special_chars = re.sub(r'[^a-z0-9\s]', ' ', normalized)
    word_list = without_special_chars.split()
    word_list = ' '.join(word_list)
    return word_list


def tokenize(item):
    '''tokenize all the words in the string, item'''
    tokenizer = nltk.tokenize.ToktokTokenizer()
    new_item = tokenizer.tokenize(item, return_str=True)
    return new_item


def print_stop_words(item):
    '''accept some text, apply stemming to all of the words,
        and print a list of value counts for all the stemmed words'''
    # Create the nltk stemmer object, then use it
    ps = nltk.porter.PorterStemmer()
    stems = [ps.stem(word) for word in item.split()]
    print(pd.Series(stems).value_counts())


def stem(item):
    '''accept a string and return it after applying stemming to all the words'''
    ps = nltk.stem.PorterStemmer()
    item_stemmed = ''.join([ps.stem(word) for word in item])
    return item_stemmed


def lemmatize(item):
    '''accept a string and return it after applying lemmatization to each word.'''
    wnl = nltk.stem.WordNetLemmatizer()
    lemmatized_words = [wnl.lemmatize(word) for word in item]

    item_lemmatized = ''.join(lemmatized_words)
    return item_lemmatized


def remove_stopwords(item, extra_words=[], exclude_words=[]):
    '''remove all the stopwords, including all the words in extra_words and excluding
    all the words in exclude list'''
    # get basic stopword list
    stopword_list = stopwords.words('english')

    # add extra words
    stopword_list = stopword_list + extra_words
    # remove excluded words
    stopword_list = [
        word for word in stopword_list if word not in exclude_words]

    without_stopwords = [word for word in item.split(
        ' ') if word not in stopword_list]
    item_without_stopwords = ' '.join(without_stopwords)
    return item_without_stopwords


def prep_repo_html(this_repo, extra_words=[], exclude_words=[]):
    '''
    takes in a dictionary representing an item and returns a dictionary that 
    looks like this:
        {
         'title': this_dict['title'],
         'language': this_dict['language'],
         'original': original,
         'clean': item
        }    
    '''
    # put the content section into item and make a copy
    item = this_repo['content']
    original = item

    '''
    apply some basic text cleaning to the string, item:
        - lowercase everything
        - normalize unicode characters
        - replace anything that is not a letter, number, whitespace or a single quote
    '''
    item = basic_clean(item)

    # '''tokenize all the words in the string, item'''
    item = tokenize(item)

    # ''''apply lemmatization to each word in the string, item'''
    lemmad = lemmatize(item)

    # apply stemming to each word in string, item
    stemmed = stem(item)

    '''remove all the stopwords, including all the words in extra_words and excluding
    all the words in exclude list'''
    # remove numeral characters
    lemmad = re.sub(r'[0-9]', '', lemmad)
    stemmed = re.sub(r'[0-9]', '', stemmed)
    # remove stopwords
    lemmad = remove_stopwords(item, extra_words, exclude_words)
    stemmed = remove_stopwords(item, extra_words, exclude_words)
    # regroom numerals after removing stopwords in case of violated formatting as  a result
    lemmad = re.sub(r'[0-9]\s', '', lemmad)
    stemmed = re.sub(r'[0-9]\s', '', stemmed)
    lemmad = re.sub(r'[^A-Za-z\s]', '', lemmad)
    stemmed = re.sub(r'[^A-Za-z\s]', '', stemmed)
    
    keys = list(this_repo.keys())

    new_dict = {
        'title': this_repo['title'],
        'language': this_repo['language'],
        'original': original,
        'lemmatized': lemmad,
        'stemmed': stemmed
    }
    return new_dict


def prepare_repo_html_data(items, extra_words=None, exclude_words=None):

    # takes in the list of items dictionaries,
    # applies the prep_item function to each one,
    # and returns the transformed data.
    transformed_items = []
    for item_index in range(len(items)):
        transformed_entry = prep_repo_html(
            items[item_index], extra_words, exclude_words)
        transformed_items.append(transformed_entry.copy())
        df = pd.DataFrame.from_dict(transformed_items)

    return transformed_items, df
