import requests
from bs4 import BeautifulSoup

response = requests.get('https://www.happiestminds.com/news-and-events/press-releases/').text

soup = BeautifulSoup(response, 'lxml')

tech_box = soup.find_all(class_='tech_box')

for box in tech_box:
    headline = box.find('a')
    print(headline.text)
    date = box.find_all('p')[1].text
    print(date)
    print()