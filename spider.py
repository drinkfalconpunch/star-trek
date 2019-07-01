from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
import os
from pathlib import Path
from bs4 import BeautifulSoup
from time import sleep

class StarTrekSpider():
    _classes = {"tng": "dhtgD"}
    _xpath = '//*[contains(@class, "{}")]'
    _url = 'https://sites.google.com/site/tvwriting/us-drama/show-collections/star-trek-{}'

    def __init__(self, url, series, driver=None, browser='chrome'):
        if not series:
            ValueError('Series needed for spider.')
        if not url:
            ValueError('URL needed for scraping.')
        self.url_to_crawl = url.format(series)
        self.xpath = self._xpath.format(self._classes[series])
        self.items = []
        # self.options = Options()
        self.browser = browser

    def __enter__(self):
        self.open_webdriver()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        # from https://docs.quantifiedcode.com/python-anti-patterns/correctness/exit_must_accept_three_arguments.html
        self.close_webdriver()

    def open_webdriver(self):
        if self.browser.lower() == 'chrome':
            self.driver = webdriver.Chrome('chromedriver', chrome_options=self.options)
        elif self.browser.lower() == 'firefox':
            self.driver = webdriver.Firefox()
        else:
            raise ValueError('Invalid browser.')
        print('Webdriver opened')
        sleep(2)

    def close_webdriver(self):
        self.driver.quit()
        print('Webdriver closed')

    def get_url(self, url=None):
        url = self.url_to_crawl if not url else url
        self.driver.get(url)

    def get_scripts(self, url=None, folder=None):
        try:
            os.makedirs(folder)
        except OSError as e:
            # Check is error is directory exists and if so continue, else raise error.
            import errno
            if e.errno != errno.EEXIST:
                raise

        try:
            pwd = Path.cwd() / folder
        except TypeError:
            pwd = Path.cwd()

        self.get_url(url)
        for s in self.driver.find_elements_by_xpath(self.xpath):
            # Get the redirect from the original page to where the pdf is located
            r = requests.get(s.get_attribute('href'), allow_redirects=True)

            # Load the content for parsing with bs4
            soup = BeautifulSoup(r.content, 'lxml')

            # Get the url from the meta HTML tag
            file = soup.find_all('meta')[1]['content'][7:]
            r = requests.get(file)

            # Save the file to disk
            open(pwd / s.text, 'wb').write(r.content)


class StarTrekSpider2():
    _url = 'https://scifi.media/star-trek/transcripts/'
    _series = {'movies', 'ds9', 'tng', 'tos', 'voyager', 'enterprise'}

    def __init__(self, series=None):
        self.series = series

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def get_scripts(self, folder=None):
        try:
            os.makedirs(folder)
        except OSError as e:
            # Check is error is directory exists and if so continue, else raise error.
            import errno
            if e.errno != errno.EEXIST:
                raise

        try:
            pwd = Path.cwd() / folder
        except TypeError:
            pwd = Path.cwd()

        r = requests.get(self._url)
        soup = BeautifulSoup(r.content, 'lxml')
        section = soup.find('div', id=self.series).next_sibling
        links = section('a')

        print('Downloading...')
        for link in links:
            s = requests.get(link['href'])
            link_string = link.string
            try:
                link_string = link.string.replace(":", "-")
            except:
                pass
            open(pwd / f'{link_string}.txt', 'wb').write(s.content)

        print('Finished downloading')