import requests
from bs4 import BeautifulSoup

response = requests.get('https://www.tatapower.com/media/media-releases.aspx?utm_medium=301&utm_source=direct&utm_campaign=/media/media-releases.aspx').text

soup = BeautifulSoup(response, 'lxml')

list_news = soup.find(class_="cont-search-results").find('ul').find_all('li')

# print(list_news)

for news in list_news:
    location = news.find('b')
    headline = news.find('p')
    print("Location: " + location.text)
    print("Headline: " + headline.text)
    print()
