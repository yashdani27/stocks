import requests
from bs4 import BeautifulSoup

response = requests.get('https://www.tataconsumer.com/media/news').text

soup = BeautifulSoup(response, 'lxml')

list_items = soup.find(class_="views-infinite-scroll-content-wrapper").find('ul').find_all('li')

for item in list_items:
    print(item.find('a').text.strip())
    print(item.find(class_="card__date").text.strip())

