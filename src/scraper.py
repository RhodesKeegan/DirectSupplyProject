import time
from random import random, randrange

from bs4 import BeautifulSoup
import pandas as pd
import requests

class Scraper:
    def __init__(self, search_words, num_results):
        self.search_words = search_words
        self.found_links = []
        self.num_results = num_results

    def get_links(self):
        # Setting everything up
        url = f'https://google.com/search?q={self.search_words}&num={self.num_results}'


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
        self.found_links = cleaned_links

        # The next step to this is to add the function to have this go through x number of google pages and then
        # Actually scrape the provided generic_search_data

    def data_scrape(self):
        '''
        Ight so this is how it's gonna go. First we are going to check all usual suspects for certain key words
        In this case we are going to check all header elements, paragraph elements, div elements, span elements
        maybe table generic_search_data if needed.

        After we check these for keywords, if they contain these keywords then we will further interrogate them
        by actually getting generic_search_data from it. We are also going to check all children element of the match in case
        we will miss out on certain elements that may be present in something like a list within a div.
        If no keywords are detected, then we ignore it and move on. This will be put into some sort of a generic_search_data structure,
        either in this method or some other method, and then that generic_search_data will most likely need to be cleaned
        '''

        key_words = ('filter', 'coil', 'fan', 'repair', 'maintenance')
        count = 54


        for link in self.found_links[55:]:

            #if link not in self.visited_links:
            count += 1
            print("Working on link number " + str(count))
            found_words = {}

            soup = BeautifulSoup(requests.get(link).text, 'html.parser')
            print("I am after the soup creation")

            time.sleep((random() + randrange(3)) * random()+6)

            for key_word in key_words:

                h3 = soup.find_all('h3', text=lambda x: x and key_word in x.lower())
                h2 = soup.find_all('h2', text=lambda x: x and key_word in x.lower())
                p = soup.find_all('p', text=lambda x: x and key_word in x.lower())
                div = soup.find_all('div', text=lambda x: x and key_word in x.lower())
                h1 = soup.find_all('h1', text=lambda x: x and key_word in x.lower())
                span = soup.find_all('span', text=lambda x: x and key_word in x.lower())
                li = soup.find_all('li', text=lambda x: x and key_word in x.lower())

                found_words['h3 ' + key_word] = map(lambda x: x.get_text(), h3)
                found_words['h2 ' + key_word] = map(lambda x: x.get_text(), h2)
                found_words['p ' + key_word] = map(lambda x: x.get_text(), p)
                found_words['div ' + key_word] = map(lambda x: x.get_text(), div)
                found_words['h1 ' + key_word] = map(lambda x: x.get_text(), h1)
                found_words['span ' + key_word] = map(lambda x: x.get_text(), span)
                found_words['li ' + key_word] = map(lambda x: x.get_text(), li)

            self.store_data(found_words, count)




    def store_data(self, data, count):
        df = pd.DataFrame.from_dict(data, orient='index')
        df = df.transpose()
        df.to_csv('./generic_search_data/link' + str(count) + '.csv')


