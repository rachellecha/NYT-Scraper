import requests

API_KEY = #dummy_key

def build_url(API_KEY, domain):
    base_url = 'http://newsapi.org/v2/everything?domains='

    key = '&apiKey=' + API_KEY
    url = base_url + domain + key
    return url

def get_json(url):
    page = requests.request('GET', url)
    output = page.json()
    return output

class news_api():

    def __init__(self, API_KEY):
        
        self.key = API_KEY
    
    def get_domains(self):
        
        # This method can be used to get a list of all available domains.
        # It will return a JSON file that can be parsed for all English-language domains.
        
        url = 'https://newsapi.org/v2/sources?language=en&apiKey=' + str(self.key)
        domains_json = get_json(url)
        return domains_json

    def get_news(self, domain):
        
        # This method can be used to get all news (up to 6 months old) from a given domain.
        # 'domain" input is a str.
        # Output is a JSON with all news data.
        
        url = build_url(self.key, domain)
        news_json = get_json(url)
        return news_json

client = news_api(API_KEY)
#print(client.get_domains())
response = client.get_news('washingtonpost.com')
print(response)
