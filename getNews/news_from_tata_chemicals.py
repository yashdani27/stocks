import requests
from bs4 import BeautifulSoup

response = requests.get('https://www.tatachemicals.com/news-room/press-release').text

soup = BeautifulSoup(response, 'lxml')

list_news = soup.find_all(class_="border_wrapper")[3:]

# print(list_news)

for news in list_news:
    headline = news.find('a')
    location = news.find('p')
    print("Date: " + location.text.strip())
    print("Headline: " + headline.text)
    print('///////////////////////////////////////////////////////////////')
