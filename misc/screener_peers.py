import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

# url = 'https://www.screener.in/company/compare/00000057/00000085/?page=1' steel
# url = 'https://www.screener.in/company/compare/00000046/00000072/?page=1' pharma
# url = 'https://www.screener.in/company/compare/00000034/00000028/?page=1' # it
url = 'https://www.screener.in/company/compare/00000016/00000031/?page=1' #construction

html_response = requests.get(url).text

# print(html_response)

soup = BeautifulSoup(html_response, 'lxml')
# , 'flex-row', 'flex-gap-8', 'flex-space-between', 'flex-align-center'
pages = soup.find_all(True, {'class': ['font-size-14', 'font-weight-500', 'sub']})
# sub = pages.find(class_="sub")
print([p.text for p in pages])
number_of_pages = int(pages[9].text.strip()[:-1].split(' ')[3])
print(number_of_pages)

set_link = set([])

# base_url = 'https://www.screener.in/company/compare/00000057/00000085/?page='
# base_url = 'https://www.screener.in/company/compare/00000046/00000072/?page='
# base_url = 'https://www.screener.in/company/compare/00000034/00000028/?page=1'
base_url = 'https://www.screener.in/company/compare/00000016/00000031/?page=' #construction
for i in range(number_of_pages):
    url = base_url + str(i + 1)
    print(url)
    html_response = requests.get(base_url).text
    soup = BeautifulSoup(html_response, 'lxml')
    pages = soup.find_all(True, {'class': ['font-size-14', 'font-weight-500', 'sub']})
    # sub = pages.find(class_="sub")
    print([p.text for p in pages])
    number_of_pages = int(pages[9].text.strip()[:-1].split(' ')[3])
    rows = soup.find(True, {'class': ['responsive-holder', 'fill-card-width']}).find_all('tr')
    for r in rows:
        data = r.find_all('td')
        if len(data) > 0:
            company_name = data[1]
            link = company_name.find('a')['href']
            set_link.add(company_name.text.strip())
            # print(data[0].text + company_name.text.strip() + ' | ' + link)
    # print([r for r in rows])
    print(len(rows))
    time.sleep(1)
print(set_link)
df_link = pd.DataFrame(list(set_link))
df_link.columns = ['Companies']
print(df_link)
df_link.to_csv(r'/Users/dharmendradani/PycharmProjects/ScreenerPeers.csv')