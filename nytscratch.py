from bs4 import BeautifulSoup
import urllib.request,sys,time
import requests
import pandas as pd
import numpy as np


def get_body(URL):
    #url of the page that we want to Scarpe
    #Use the browser to get the URL. This is a suspicious command that might blow up.

    try:
        # this might throw an exception if something goes wrong.
        page=requests.get(URL) 
        # this describes what to do if an exception is thrown
        
    except Exception as e:    
        
        # get the exception information
        error_type, error_obj, error_info = sys.exc_info()      
        
        #print the link that cause the problem
        print ('ERROR FOR LINK:',URL)
        
        #print error info and line that threw the exception                          
        print (error_type, 'Line:', error_info.tb_lineno)
        
    news_contents = []

    content = page.text
    soup = BeautifulSoup(content, 'html5lib')

    body = soup.find_all('div', class_="css-1fanzo5 StoryBodyCompanionColumn")


    leng = len(body)
    i = 0
        
    list_paragraphs = []

    while (i < leng):
        x = body[i].find_all('p')

        for p in np.arange(0, len(x)):
            paragraph = x[p].get_text()
            list_paragraphs.append(paragraph)
            final_article = " ".join(list_paragraphs)
        
        i+=1
            
    news_contents.append(final_article)
    #print(news_contents)
    return(news_contents)

def get_sum(URL):
    #url of the page that we want to Scarpe
    #Use the browser to get the URL. This is a suspicious command that might blow up.

    try:
        # this might throw an exception if something goes wrong.
        page=requests.get(URL) 
        # this describes what to do if an exception is thrown
        
    except Exception as e:    
        
        # get the exception information
        error_type, error_obj, error_info = sys.exc_info()      
        
        #print the link that cause the problem
        print ('ERROR FOR LINK:',URL)
        
        #print error info and line that threw the exception                          
        print (error_type, 'Line:', error_info.tb_lineno)
        
    content = page.text
    soup = BeautifulSoup(content, 'html5lib')

    try: 
        '''
        sum = soup.find_all('p', id_="article-summary")
        if (sum[0].text):
            sub = sum[0].text
        else:
            sub = 'n/a'
        '''
        sum = soup.find_all('p', class_="css-1smgwul e1wiw3jv0") 
        if (sum[0].text):
            sub = sum[0].text
        else:
            sub = 'n/a'

    except:
        sub = 'n/a'

    #print(sub)   

    return(sub)


data = pd.read_csv("2020-5.csv")
body = []
summ = []
author = []


for index, row in data.iterrows():
    URL = row["web_url"]
    text = get_body(URL)
    summary = get_sum(URL)
    body.append(text)
    summ.append(summary)

data = data.assign(body = body, summary = summ)

data.to_csv(r'2020-5.csv')


'''
URL = 'https://www.nytimes.com/2020/10/03/world/europe/brexit-deal-talks.html'

try:
        # this might throw an exception if something goes wrong.
    page=requests.get(URL) 
        # this describes what to do if an exception is thrown
        
except Exception as e:    
        
        # get the exception information
    error_type, error_obj, error_info = sys.exc_info()      
        
        #print the link that cause the problem
    print ('ERROR FOR LINK:',URL)
        
        #print error info and line that threw the exception                          
    print (error_type, 'Line:', error_info.tb_lineno)
        
news_contents = []

content = page.text
soup = BeautifulSoup(content, 'html5lib')

try: 
    
    #sum = soup.find_all('p', id_="article-summary")
    #if (sum[0].text):
        #sub = sum[0].text
    #else:
        #sub = 'n/a'

    sum = soup.find_all('p', class_="css-1smgwul e1wiw3jv0") 
    if (sum[0].text):
        sub = sum[0].text
    else:
        sub = 'n/a'

except:

    sub = 'n/a'


print(sub)
'''