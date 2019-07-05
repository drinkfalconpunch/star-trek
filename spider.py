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

    async def _fetch_and_save_async(self, session, url, file_name, path, chunk_size=1000):
        file_path = path / file_name
        async with session.get(url) as resp:
            if resp.status != 200:
                resp.raise_for_status()
            with open(file_path, 'wb') as fd:
                while True:
                    chunk = await resp.content.read(chunk_size)
                    if not chunk:
                        break
                    fd.write(chunk)

    def _mkdir(self, folder=None):
        pwd = Path('.')
        if folder:
            pwd = pwd / folder / self.series
        else:
            pwd = pwd / self.series
        pwd.mkdir(parents=True, exist_ok=True)

        return pwd

    async def _get_scripts(self, folder=None):
        tasks = []
        path = self._mkdir(folder)
        names_with_urls = self._collect_download_names_urls()

        async with aiohttp.ClientSession() as session:
            for file_name, url in names_with_urls.items():
                # pass Semaphore and session to every GET request
                task = asyncio.ensure_future(
                    self._fetch_and_save_async(session, url, file_name, path)
                )
                tasks.append(task)

            responses = asyncio.gather(*tasks)
            await responses

    def get_scripts_async(self, folder=None):
        loop = asyncio.get_event_loop()
        print('Downloading...')
        future = loop.create_task(self._get_scripts(folder))
        loop.run_until_complete(future)
        print('Finished downloading.')

    def get_scripts(self, folder=None):
        path = self._mkdir(folder)
        names_with_urls = self._collect_download_names_urls()
        print('Downloading...')
        for file_name, url in names_with_urls.items():
            self._fetch_and_save(url, file_name, path)
        print(f'Finished downloading. Scripts saved in {path.absolute()}')
