from scraper import Scraper


def main():
    scraper = Scraper('ptac maintenance diy', 1000)
    scraper.get_links()
    scraper.data_scrape()

if __name__ == '__main__':
    main()