'''
import os
import json
import time
import requests
import datetime
import dateutil
import pandas as pd
from dateutil.relativedelta import relativedelta

end = datetime.date.today()
start = end - relativedelta(years=1)

months_in_range = [x.split(' ') for x in pd.date_range(start, end, freq='MS').strftime("%Y %-m").tolist()]

def send_request(query, filters):
    #Sends a request to the NYT Archive API for given date.
    base_url = 'https://api.nytimes.com/svc/search/v2/'
    url = base_url + 'articlesearch' + '.json?q=' + query + '&fq=' + filters + '&api-key=' + "mlb01Pu6lzIngAwgzBXDp3pa1CteNK8g"
    response = requests.get(url).json()
    time.sleep(6)
    return response


def parse_response(response):
    #Parses and returns response as pandas data frame.
    data = {'headline': [],  
        'snippet': [],
        'news_desk': [],
        'keywords': []}
    
    articles = response['response']['docs'] 
    for article in articles: # For each article, make sure it falls within our date range
        data['headline'].append(article['headline']['main']) 
        if 'news_desk' in article:
            data['news_desk'].append(article['news_desk'])
        else:
            data['news_desk'].append(None)
        if 'snippet' in article: 
            data['snippet'].append(article['snippet'])
        else:
            data['snippet'].append(None)
        keywords = [keyword['value'] for keyword in article['keywords'] if keyword['name'] == 'subject']
        data['keywords'].append(keywords)
    return pd.DataFrame(data) 


def get_data(q, fq):
    #Sends and parses request/response to/from NYT Archive API for given dates.
    total = 0
    #print('Date range: ' + str(dates[0]) + ' to ' + str(dates[-1]))
    if not os.path.exists('headlines'):
        os.mkdir('headlines')
 
    response = send_request(q, fq)
    df = parse_response(response)
    total += len(df)
    df.to_csv('nyt.csv', index=False)
        #print('Saving headlines/' + date[0] + '-' + date[1] + '.csv...')
    #print('Number of articles collected: ' + str(total))


q = "Israel"
fq = 'source:("The New York Times") AND news_desk:("World")'


get_data(q, fq)
'''

import os
import json
import time
import requests
import datetime
import dateutil
import pandas as pd
from dateutil.relativedelta import relativedelta


def send_request(date):
    '''Sends a request to the NYT Archive API for given date.'''
    base_url = 'https://api.nytimes.com/svc/archive/v1/'
    url = base_url + '/' + date[0] + '/' + date[1] + '.json?api-key=' + 'mlb01Pu6lzIngAwgzBXDp3pa1CteNK8g'
    response = requests.get(url).json()
    time.sleep(6)
    return response


def is_valid(article, date):
    '''An article is only worth checking if it is in range, and has a headline.'''
    is_in_range = date > start and date < end
    has_headline = type(article['headline']) == dict and 'main' in article['headline'].keys()
    return is_in_range and has_headline


def parse_response(response):
    '''Parses and returns response as pandas data frame.'''
    data = {'headline': [],  
        'date': [], 
        'doc_type': [],
        'web_url': [],
        'news_desk': [],
        'keywords': [],
        'byline': []}
    
    articles = response['response']['docs'] 
    for article in articles: # For each article, make sure it falls within our date range
        date = dateutil.parser.parse(article['pub_date']).date()
        if is_valid(article, date):
            data['date'].append(date)
            data['headline'].append(article['headline']['main']) 
            if 'news_desk' in article:
                data['news_desk'].append(article['news_desk'])
            else:
                data['news_desk'].append(None)
            data['doc_type'].append(article['document_type'])
            if 'web_url' in article: 
                data['web_url'].append(article['web_url'])
            else:
                data['web_url'].append(None)
            if 'byline' in article:
                data['byline'].append(article['byline']['original'])
            else:
                data['byline'].append(None)
            keywords = [keyword['value'] for keyword in article['keywords'] if keyword['name'] == 'subject']
            data['keywords'].append(keywords)
    return pd.DataFrame(data) 


def get_data(dates):
    '''Sends and parses request/response to/from NYT Archive API for given dates.'''
    total = 0
    print('Date range: ' + str(dates[0]) + ' to ' + str(dates[-1]))
    if not os.path.exists('headlines'):
        os.mkdir('headlines')
    for date in dates:
        response = send_request(date)
        df = parse_response(response)
        total += len(df)
        df.to_csv('headlines/' + date[0] + '-' + date[1] + '.csv', index=False)
        print('Saving headlines/' + date[0] + '-' + date[1] + '.csv...')
    print('Number of articles collected: ' + str(total))

end = datetime.date.today()
start = end - relativedelta(years=1)
months_in_range = [x.split(' ') for x in pd.date_range(start, end, freq='MS').strftime("%Y %-m").tolist()]

get_data(months_in_range)