from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
from time import sleep

class StarTrekSpider():
    _classes = {"tng": "dhtgD"}
    _xpath = '//*[contains(@class, "{}")]'

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
        sleep(3)

    def close_webdriver(self):
        self.driver.quit()
        print('Webdriver closed')

    def get_url(self, url=None):
        if not url:
            url = self.url_to_crawl
        self.driver.get(url)

    def get_scripts(self, url=None):
        self.get_url(url)
        for s in self.driver.find_elements_by_xpath(self.xpath)[:5]:
            # Get the redirect from the original page to where the pdf is located
            r = requests.get(s.get_attribute('href'), allow_redirects=True)

            # Load the content for parsing with bs4
            soup = BeautifulSoup(r.content, 'lxml')

            # Get the url from the meta HTML tag
            file = soup.find_all('meta')[1]['content'][7:]
            r = requests.get(file)

            # Save the file to disk
            open(f'{s.text}', 'wb').write(r.content)