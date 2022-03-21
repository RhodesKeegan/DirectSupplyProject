from bs4 import BeautifulSoup
import requests

class Scraper:
    def __init__(self, search_words):
        self.search_words = search_words

    def scrape(self):
        url = 'https://google.com/search?q=' + self.search_words
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        links = soup.findAll('a')
        unfiltered_links = []
        for link in links:
            unfiltered_links.append(link.get('href'))

