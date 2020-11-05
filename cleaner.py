import pandas as pd

data = pd.read_csv("2019-12.csv")

#index_names = data[ (data['news_desk'] != "Foreign")].index


#data.drop(index_names, inplace = True)

#data.drop([ 'web_url'], axis=1, inplace=True)

#data.drop_duplicates(subset=['headline'])

#print(data)

data.rename(columns={"headline": "title", "byline": "author"})

data.to_csv(r'2019-12.csv', index = False)

