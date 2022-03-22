from bs4 import BeautifulSoup
import requests
from functools import reduce

class Scraper:
    def __init__(self, search_words):
        self.search_words = search_words
        self.found_links = {}

    def get_links(self):
        # Setting everything up
        url = 'https://google.com/search?q=' + self.search_words


        soup = BeautifulSoup(requests.get(url).text, 'html.parser')

        # Finding all links on the page and then removing non-relevant links found
        links = soup.findAll('a')


        links = list(filter(lambda x: '/url?q=https://www.youtube.com' not in x.get('href') and 'google.com'\
                            not in x.get('href'), links))

        # Adding links to temp list and then adding that list to the dictionary
        cleaned_links = []
        for link in links:
            if 'https://' in link.get('href'):
                href = link.get('href')
                temp_link = href[href.find('=')+1:href.find('&')]
                cleaned_links.append(temp_link)
        self.found_links['Page 1'] = cleaned_links

        # The next step to this is to add the function to have this go through x number of google pages and then
        # Actually scrape the provided data

    def data_scrape(self):
        pass
