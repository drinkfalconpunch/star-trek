from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
from time import sleep

class StarTrekSpider():
    _classes = {"tng": "dhtgD"}
    _xpath = "//*[@class=\"{}\"]"
    
    def __init__(self, url, series, driver=None, browser='chrome'):
        if not series:
            ValueError('Series needed for spider.')
        if not url:
            ValueError('URL needed for scraping.')
        self.url_to_crawl = url.format(series)
        self.xpath = self._xpath.format(self._classes[series])
        self.items = []
        self.options = Options()
        self.browser = browser
        self.options.add_experimental_option("prefs", {
            "plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],
            "download.default_directory": r"C:\Users\John Hudson\Code\star-trek\test",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
    
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
    
    def _populate_dictionary(self, xpath, url=None):
        self.get_url(url)
        for s in self.driver.find_elements(By.XPATH, xpath)[:4]:
            soup = BeautifulSoup(s.content, 'lxml')
            file = soup.find_all('meta')[1]['content'][7:]
            r = requests.get(file)
            open(f'{s.text}', 'wb').write(r.content)
            # s.get_attribute("href")
            r = requests.get(s.get_attribute("href"))#, r"C:\Users\John Hudson\Code\star-trek\test\{}".format(s.text)
            soup = BeautifulSoup(r.content, 'lxml')
            print(soup)
#             file = open(f'{s.text}', 'wb')
#             for chunk in r.iter_content(100000):
#                 file.write(chunk)