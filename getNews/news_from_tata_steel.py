from getNews.soup import get_soup

soup = get_soup('https://www.tatasteel.com/media/newsroom/press-releases/')

cards = soup.find_all(class_="card")

for card in cards:
    print("headline: " + card.find('strong').text)
    print("place: " + card.find(class_="date-day").find_all('span')[0].text)
    print("date: " + card.find(class_="date-day").find_all('span')[1].text)
    print()
