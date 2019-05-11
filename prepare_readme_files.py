# Preparation
from acquire_msc import get_all_readme_files_and_languages
import unicodedata
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import pandas as pd


def basic_clean(article):
    '''
    take in a string (article) and return it after applying some basic text cleaning to it:
        - lowercase everything
        - normalize unicode characters
        - replace anything that is not a letter, number, whitespace or a single quote
    '''
    new_article = article.lower()
    new_article = re.sub(r'\s', ' ', new_article)
    normalized = unicodedata.normalize('NFKD', new_article)                .encode('ascii', 'ignore')                .decode('utf-8')
    without_special_chars = re.sub(r'[^\w\s]', ' ', normalized)
    word_list = without_special_chars.split()
    word_list = ' '.join(word_list)
    return word_list


def tokenize(article):
    '''tokenize all the words in the string, article'''
    tokenizer = nltk.tokenize.ToktokTokenizer()
    new_article = tokenizer.tokenize(article, return_str=True)
    return new_article


def print_stop_words(article):
    '''accept some text, apply stemming to all of the words,
        and print a list of value counts for all the stemmed words'''
    # Create the nltk stemmer object, then use it
    ps = nltk.porter.PorterStemmer()
    stems = [ps.stem(word) for word in article.split()]
    print(pd.Series(stems).value_counts())


def stem(article):
    '''accept a string and return it after applying stemming to all the words'''
    ps = nltk.stem.PorterStemmer()
    article_stemmed = ''.join([ps.stem(word) for word in article])
    return article_stemmed


def lemmatize(article):
    '''accept a string and return it after applying lemmatization to each word.'''
    wnl = nltk.stem.WordNetLemmatizer()
    lemmatized_words = [wnl.lemmatize(word) for word in article]
    article_lemmatized = ''.join(lemmatized_words)
    return article_lemmatized


def remove_stopwords(article, extra_words = [], exclude_words = []):
    '''remove all the stopwords, including all the words in extra_words and excluding
    all the words in exclude list'''
    # get basic stopword list
    stopword_list = stopwords.words('english')

    # add extra words    
    stopword_list = stopword_list + extra_words
    # remove excluded words
    stopword_list = [word for word in stopword_list if word not in exclude_words]
    
    without_stopwords = [word for word in article.split(' ') if word not in stopword_list]
    article_without_stopwords = ' '.join(without_stopwords)
    return article_without_stopwords


def prep_repo_html(this_repo, extra_words = [], exclude_words = []):
    '''
    takes in a dictionary representing an article and returns a dictionary that 
    looks like this:
        {
         'title': this_dict['title'],
         'language': this_dict['language'],
         'original': original,
         'clean': article
        }    
    '''
    # put the content section into article and make a copy
    article = this_repo['content']
    original = article

    '''
    apply some basic text cleaning to the string, article:
        - lowercase everything
        - normalize unicode characters
        - replace anything that is not a letter, number, whitespace or a single quote
    '''
    article = basic_clean(article)

    '''tokenize all the words in the string, article'''
    article = tokenize(article)
    
    ''''apply lemmatization to each word in the string, article'''
    article = lemmatize(article)
    
    '''remove all the stopwords, including all the words in extra_words and excluding
    all the words in exclude list'''
    article = remove_stopwords(article, extra_words, exclude_words)

# should add this code to remove any repos that do not have languages listed, 
# but don't have any such repos right now.
    # removing all rows that has 'No language specified.'
#     df = df[df.language != 'No language specified.']
#     df = df.rename(index=str, columns={"clean": "text"})
    
    keys = list(this_repo.keys())
    
    new_dict = {
         'title': this_repo['title'],
         'language': this_repo['language'],
         'original': original,
         'clean': article
        }
    return new_dict


def prepare_repo_html_data(articles, extra_words = None, exclude_words = None):
        
    # takes in the list of articles dictionaries, 
    # applies the prep_article function to each one, 
    # and returns the transformed data.
    transformed_articles = []
    for article_index in range(len(articles)):
        transformed_entry = prep_repo_html(articles[article_index], extra_words, exclude_words)
        transformed_articles.append(transformed_entry.copy())
        df = pd.DataFrame.from_dict(transformed_articles)

    return transformed_articles, df
