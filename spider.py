# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
import aiohttp
import requests
import os
from pathlib import Path
from bs4 import BeautifulSoup
from time import sleep
import asyncio

WINDOWS_CHARS = '<>:\"\\/|?*'


class StarTrekSpider():
    _url = 'https://scifi.media/star-trek/transcripts/'
    _series = {'movies', 'ds9', 'tng', 'tos', 'voyager', 'enterprise'}
    _series_ranges = {
        'movies':     range(9, 11),
        'tng':        range(18, 25),
        'ds9':        range(32, 39),
        'voyager':    range(46, 53),
        'enterprise': range(60, 64),
        'tos':        range(71, 74)
    }

    def __init__(self, series=None):
        if not series in self._series:
            raise ValueError(f'Invalid series {series}. {self._series}')
        self.series = series

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    async def _fetch_content2(self, session, url):
        async with session.get(url) as response:
            if response.status != 200:
                response.raise_for_status()
            return await response.content

    def _extract_name_url(self, blob):
        file_name = blob.text + '.txt'
        download_url = blob['href']

        # Remove all the special chars that piss windows off
        for ch in WINDOWS_CHARS:
            if ch in file_name:
                if ch == ':':
                    # Replace colons with dashes
                    file_name = file_name.replace(ch, " -")
                else:
                    file_name = file_name.replace(ch, '')

        return file_name, download_url

    def _collect_download_names_urls(self):
        downloads = {}

        r = requests.get(self._url)
        soup = BeautifulSoup(r.content, 'lxml')

        ranges = soup.find_all(
            'div',
            {'class': [f'fusion-builder-column-{c}' for c in self._series_ranges[self.series]]}
        )

        for i in ranges:
            for j in i.find_all('a'):
                file_name, download_url = self._extract_name_url(j)
                downloads[file_name] = download_url

        return downloads

    def _save_script(self, content, file_name, path):
        file_path = path / file_name
        open(file_path, 'wb').write(content)

    def _fetch_content(self, url):
        r = requests.get(url)
        if r.status_code != 200:
            r.raise_for_status()
        return r.content

    def _fetch_and_save(self, url, file_name, path):
        content = self._fetch_content(url)
        self._save_script(content, file_name, path)

    async def _fetch_and_save2(self, session, url, file_name, path):
        content = await self._fetch_content(session, url)
        await self._save_script(content, file_name, path)

    async def _write_url_to_file(self, download_url):
        async with aiohttp.ClientSession() as client:
            return await self._fetch_content(client, download_url)

    def _mkdir(self, folder=None):
        pwd = Path('.')
        if folder:
            pwd = pwd / folder / self.series
        else:
            pwd = pwd / self.series
        pwd.mkdir(parents=True, exist_ok=True)

        return pwd

    async def _get_scripts(self, folder=None):
        # if not series:
        #     series = self.series
        print(1)
        pwd = Path('.')
        if folder:
            pwd = pwd / folder / self.series
        else:
            pwd = pwd / self.series
        pwd.mkdir(parents=True, exist_ok=True)
        print(2)
        names_with_urls = self._collect_download_names_urls()
        print(5)

        sem = asyncio.Semaphore(1000)

        async with aiohttp.ClientSession() as session:
            tasks = []
            for file_name, download_url in names_with_urls.items():
                tasks.append(
                    self._fetch_and_save(
                        session=session,
                        url=download_url,
                        file_name=file_name,
                        path=pwd
                    )
                )
            # asyncio.gather() will wait on the entire task set to be
            # completed.  If you want to process results greedily as they come in,
            # loop over asyncio.as_completed()
            stuff = await asyncio.gather(*tasks, return_exceptions=True)
            return stuff

    def get_scripts_async(self, folder=None):
        loop = asyncio.get_event_loop()
        print('Downloading...')
        future = asyncio.create_task(self._get_scripts(folder))
        print('Finished downloading.')
        loop.run_until_complete(future)

    def get_scripts(self, folder=None):
        path = self._mkdir(folder)
        names_with_urls = self._collect_download_names_urls()
        print('Downloading...')
        for file_name, url in names_with_urls.items():
            self._fetch_and_save(url, file_name, path)
        print(f'Finished downloading. Scripts saved in {path.absolute()}')


        # for file_name, download_url in names_with_urls:
        #     content = await self._write_url_to_file(download_url)
        #     self._save_script(content, file_name, pwd)
        # colors = ['red', 'blue', 'green']  # ...
        # # Either take colors from stdin or make some default here
        # asyncio.run(main(colors))


# class StarTrekSpider():
#     _classes = {"tng": "dhtgD"}
#     _xpath = '//*[contains(@class, "{}")]'
#     _url = 'https://sites.google.com/site/tvwriting/us-drama/show-collections/star-trek-{}'
#
#     def __init__(self, url, series, driver=None, browser='chrome'):
#         if not series:
#             ValueError('Series needed for spider.')
#         if not url:
#             ValueError('URL needed for scraping.')
#         self.url_to_crawl = url.format(series)
#         self.xpath = self._xpath.format(self._classes[series])
#         self.items = []
#         # self.options = Options()
#         self.browser = browser
#
#     def __enter__(self):
#         self.open_webdriver()
#         return self
#
#     def __exit__(self, exception_type, exception_value, traceback):
#         # from https://docs.quantifiedcode.com/python-anti-patterns/correctness/exit_must_accept_three_arguments.html
#         self.close_webdriver()
#
#     def open_webdriver(self):
#         if self.browser.lower() == 'chrome':
#             self.driver = webdriver.Chrome('chromedriver', chrome_options=self.options)
#         elif self.browser.lower() == 'firefox':
#             self.driver = webdriver.Firefox()
#         else:
#             raise ValueError('Invalid browser.')
#         print('Webdriver opened')
#         sleep(2)
#
#     def close_webdriver(self):
#         self.driver.quit()
#         print('Webdriver closed')
#
#     def get_url(self, url=None):
#         url = self.url_to_crawl if not url else url
#         self.driver.get(url)
#
#     def get_scripts(self, url=None, folder=None):
#         try:
#             os.makedirs(folder)
#         except OSError as e:
#             # Check is error is directory exists and if so continue, else raise error.
#             import errno
#             if e.errno != errno.EEXIST:
#                 raise
#
#         try:
#             pwd = Path.cwd() / folder
#         except TypeError:
#             pwd = Path.cwd()
#
#         self.get_url(url)
#         for s in self.driver.find_elements_by_xpath(self.xpath):
#             # Get the redirect from the original page to where the pdf is located
#             r = requests.get(s.get_attribute('href'), allow_redirects=True)
#
#             # Load the content for parsing with bs4
#             soup = BeautifulSoup(r.content, 'lxml')
#
#             # Get the url from the meta HTML tag
#             file = soup.find_all('meta')[1]['content'][7:]
#             r = requests.get(file)
#
#             # Save the file to disk
#             open(pwd / s.text, 'wb').write(r.content)