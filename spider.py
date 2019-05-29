from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

class StarTrekSpider():
    def __init__(self, url, xpath=None):
        self.url_to_crawl = url
        self.items = []
        
    def open_webdriver(self):
        self.driver = webdriver.Chrome('chromedriver.exe')
        print('Webdriver opened')
        sleep(5)
    
    def close_webdriver(self):
        self.driver.quit()
        print('Webdriver closed')
    
    def get_url(self, url=None):
        if not url:
            url = self.url_to_crawl
        self.driver.get(url)
        sleep(3)
    
    def _populate_dictionary(self, xpath):
        return self.driver.find_elements(By.XPATH, xpath)