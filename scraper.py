import re
import sys

from bs4 import BeautifulSoup
import requests
from requests.exceptions import ConnectionError, HTTPError, Timeout

from database import Database

'''
def error_handling(error_message: str) -> None:
    """Handle errors"""
    print(error_message)
    sys.exit(1)
'''


class ErrorHandling:
    @staticmethod
    def error_handling(error_message: str) -> None:
        """Handle errors"""
        print(error_message)
        sys.exit(1)


class Crawler:
    """Class created to define how information will be fetched"""

    _book_index_page_url = 'http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html'
    _books_numbered_url = 'http://books.toscrape.com/catalogue/category/books/sequential-art_5/page-'
    _book_link_url = 'http://books.toscrape.com/catalogue'
    _books_element_tag_name = 'li'
    _page_number_element_tag_name = 'li'
    _books_elements_class_name = 'col-xs-6 col-sm-4 col-md-3 col-lg-3'
    _page_number_element_class_name = 'current'

    def __init__(self):
        self.pages_links = []
        self.books = {}

    def get_page(self, url: str) -> BeautifulSoup:
        """Make a http get request to the passed url

        Parameter:
        A valid url

        Return:
        BeautifulSoup object
        Raise:
        HTTPError, ConnectionError, Timeout
        """
        req = None
        try:
            req = requests.get(url, timeout=60)
            req.raise_for_status()  # if the response is a 4XX client error or 5XX server error a
            # http error will be raised
        except (ConnectionError, HTTPError, Timeout) as error:
            ErrorHandling.error_handling(error.text)

        return BeautifulSoup(req.content, 'html.parser')

    def generate_pages_urls(self, soup: BeautifulSoup) -> None:
        """Based on the number of pages displayed in the end of the pages generate all pages for the category.

        Parameter:
        BeautifulSoup object.
        """
        # Number of pages information (Page 1 of 4)
        element = soup.find(self._page_number_element_tag_name, {'class': self._page_number_element_class_name})
        # Check if element was found
        if hasattr(element, 'text'):
            element = element.text.strip()
            number_of_pages = int(re.findall('[0-9]+', element)[1])
            for i in range(number_of_pages):
                self.pages_links.append(self._books_numbered_url + str(i + 1) + '.html')
        else:
            ErrorHandling.error_handling("Element not found.")

    def get_books_links(self, soup: BeautifulSoup) -> None:
        """Extracts book links from the page.

        Parameter:
        BeautifulSoup object.
        """
        # find all the links to books pages
        elements = soup.findAll(self._books_element_tag_name, {'class': self._books_elements_class_name})
        if len(elements) > 0:
            for element in elements:
                soup = self.get_page(self._book_link_url + element.find('a').get('href')[8:])
                self.books[self._book_link_url + element.find('a').get('href')[8:]] = soup
        else:
            ErrorHandling.error_handling("List of book links is empty")

    def run(self):
        """Release the crawler!"""
        page_content = self.get_page(self._book_index_page_url)
        self.generate_pages_urls(page_content)
        for page in self.pages_links:
            page_content = self.get_page(page)
            self.get_books_links(page_content)


class Scraper:
    """Class that defines how the data for each book will be extracted from the page"""

    _book_title_class_name = 'col-sm-6 product_main'
    _book_price_class_name = 'price_color'
    _book_description_id_name = 'product_description'

    def __init__(self):
        self.books_list = []
        self.store = Database()

    def extract(self, link: str, soup: BeautifulSoup) -> None:
        """Extract data from book page's
        Parameter:
        link -> url of the book page
        soup -> BeautifulSoup object of the page
        """
        book_info = {'title': None, 'price': None, 'description': None, 'url': None}
        title = soup.find('div', {'class': self._book_title_class_name})
        price = title
        description = soup.find('div', id=self._book_description_id_name)

        book_info['url'] = link
        if hasattr(title, 'text'):
            book_info['title'] = str(title.find('h1').text)
        if hasattr(price, 'text'):
            book_info['price'] = str(price.find('p').text)
        if hasattr(description, 'text'):
            book_info['description'] = str(description.findNextSibling().text)
        self.store.insert_row(book_info)  # insert the data extracted in the database

    def run(self, books: dict):
        """Run scraper
        Parameter:
        books -> dicitionary: key: book link, value: bs4 object from book page
        """
        for book in books.keys():
            val1 = book
            val2 = books[book]
            self.extract(val1, val2)


if __name__ == '__main__':
    spider = Crawler()
    spider.run()
    extractor = Scraper()
    extractor.run(spider.books)
