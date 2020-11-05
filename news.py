# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 09:31:36 2020
@author: catherinevn
"""

#News Scrape

#Import libraries
import selenium.webdriver as webdriver
import time
from bs4 import BeautifulSoup
import requests
from lxml import html
import pickle
import os
import json
from datetime import datetime
from datetime import timezone
from datetime import date as datemethod
from newsapi import NewsApiClient

# Init
newsapi = NewsApiClient(api_key= #dummy_key)

#Define functions
"""
GENERAL FUNCTIONS
"""
#get current UTC date and time as text
def get_today():
    utc_t = datetime.utcnow()
    date_str = datemethod.strftime(utc_t, '%Y%m%dZ%H%M%S')
    return date_str

#save JSON file
def save_json(file_path, json_object):
    with open(file_path, 'w') as json_file:
        json.dump(json_object, json_file)

#save object to pickle
def save_pickle(output_path, pickle_object, file_name):
    output_name = os.path.join(output_path, file_name + '.pkl')
    with open(output_name, 'wb') as pkl_object:
        pickle.dump(pickle_object, pkl_object)

#open pickle file
def open_pickle(pickle_path):
    with open(pickle_path, 'rb') as pickle_file:
        object_name = pickle.load(pickle_file, encoding='UTF-8')
    return object_name

def open_file(news_object_path):
    news_object_file = os.path.join(news_object_path, 'news_dump_object.pkl')
    if os.path.isfile(news_object_file):
        old_news = open_pickle(news_object_file)
    else:
        old_news = []
    return old_news

#url check
def url_check(old_url_set, url):
    url_set = set([url])
    test_set = old_url_set & url_set
    if len(test_set) == 0:
        check = False
    else:
        check = True
    return check

#Concat output lists
def concat_lists(out_lists):
    output = []
    for outlist in out_lists:
        output = output + outlist
    return output

"""
ASSOCIATED PRESS FUNCTIONS
"""
#get article links
def get_articles_ap(JSON):
    articles = []
    for item in JSON['articles']:
        articles.append(item)
    return articles

#get elements
def get_ap_elements(articles):
    out_list = []
    for article in articles:
            article_body = article['content']
            article_headline = article['title']
            article_description = article['description']
            article_date = article['publishedAt']
            article_link = article['url']
            out_dict = dict([('date', article_date),('time', article_date),('source','www.apnews.com'),('Title', article_headline),('Text', article_body), ('Description', article_description), ('url', article_link)])
            out_list.append(out_dict)
    return out_list

#Execute Associated Press script
def ap(data):
    print('Getting Associated Press articles...')
    articles = get_articles_ap(data)
    ap_list = get_ap_elements(articles)
    return ap_list

"""
MAIN SCRIPT
"""
def main():
    news_object_path = os.getcwd() # ?
    output_path = os.getcwd() # ?
    old_news = open_file(news_object_path)
    data = newsapi.get_everything(sources='bbc-news', language='en')
    ap_list = ap(data)
    out_lists = [old_news, ap_list]
    output_all = concat_lists(out_lists)
    print('Saving JSON...')
    today_ = get_today()
    news_object_name = os.path.join(news_object_path, today_ + 'json')
    save_json(news_object_name, ap_list)
    print("Saving news object...")
    save_pickle(output_path, output_all, 'news_dump_object')
    return ap_list

"""
EXECUTE SCRIPT
"""
if __name__ == '__main__':
    ap_list = main()
