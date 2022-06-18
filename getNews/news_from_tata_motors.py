import requests
from bs4 import BeautifulSoup

response = requests.get('https://www.tatamotors.com/media/press-releases/').text

soup = BeautifulSoup(response, 'lxml')

list_news = soup.find(class_="pressrelease_list").find_all('li')

for news in list_news:
    news_date = news.find(class_="date")
    headline = news.find('h3')
    news_body = news.find_all('p')
    # print("|" + str(type(headline)) + "|")
    if str(type(headline)) != "<class 'NoneType'>":
        print(news_date.text)
        print(headline.text)
        print(news_body[1].text)
        # print(news_body)
        print()
