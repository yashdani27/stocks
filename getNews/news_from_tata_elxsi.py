import requests
from bs4 import BeautifulSoup

response = requests.get('https://tataelxsi.com/whats-new/press-releases.html').text

soup = BeautifulSoup(response, 'lxml')

content = soup.find(id="content")

headlines = content.find_all('h6')
date = content.find_all('p')

for index, headline in enumerate(headlines):
    print(headline.find('a').text)
    print(date[index].text)
    print()