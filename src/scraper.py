from bs4 import BeautifulSoup
import requests

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
        '''
        Ight so this is how it's gonna go. First we are going to check all usual suspects for certain key words
        In this case we are going to check all header elements, paragraph elements, div elements, span elements
        maybe table data if needed.

        After we check these for keywords, if they contain these keywords then we will further interrogate them
        by actually getting data from it. We are also going to check all children element of the match in case
        we will miss out on certain elements that may be present in something like a list within a div.
        If no keywords are detected, then we ignore it and move on. This will be put into some sort of a data structure,
        either in this method or some other method, and then that data will most likely need to be cleaned
        '''

        found_words = {}



        key_words = ('filter', 'coil', 'fan', 'repair', 'maintenance')
        link_example_one = self.found_links['Page 1'][3]
        soup = BeautifulSoup(requests.get(link_example_one).text, 'html.parser')

        for key_word in key_words:

            h3 = soup.find_all('h3', text=lambda x: x and key_word in x.lower())
            h2 = soup.find_all('h2', text=lambda x: x and key_word in x.lower())
            p = soup.find_all('p', text=lambda x: x and key_word in x.lower())
            div = soup.find_all('div', text=lambda x: x and key_word in x.lower())
            h1 = soup.find_all('h1', text=lambda x: x and key_word in x.lower())
            span = soup.find_all('span', text=lambda x: x and key_word in x.lower())

            found_words['h3 ' + key_word] = h3
            found_words['h2 ' + key_word] = h2
            found_words['p ' + key_word] = p
            found_words['div ' + key_word] = div
            found_words['h1 ' + key_word] = h1
            found_words['span ' + key_word] = span


        # for element in elements:
        #     print(element.find_next_sibling('p'))


