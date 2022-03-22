from scraper import Scraper


def main():
    scraper = Scraper('ptac maintenance diy')
    scraper.get_links()

if __name__ == '__main__':
    main()