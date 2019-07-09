from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Dict, Tuple, Union

import aiohttp
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

WINDOWS_CHARS = '<>:\"\\/|?*'


class StarTrekSpider():
    _url = 'https://scifi.media/star-trek/transcripts/'
    _series_ranges = {
        'movies':     range(9, 11),
        'tng':        range(18, 25),
        'ds9':        range(32, 39),
        'voyager':    range(46, 53),
        'enterprise': range(60, 64),
        'tos':        range(71, 74)
    }

    def __init__(self, series: str = None) -> None:
        self.series = series

    def __enter__(self) -> StarTrekSpider:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @staticmethod
    def _extract_name_url(blob: Tag) -> Tuple[str, str]:
        file_name = blob.text.strip() + '.txt'
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

    def _collect_download_names_urls(self) -> Dict[str, str]:
        downloads = {}

        r = requests.get(self._url)
        soup = BeautifulSoup(r.content, 'lxml')

        ranges = soup.find_all(
            'div',
            {'class': [f'fusion-builder-column-{c}' for c in self._series_ranges[self.series]]}
        )

        for i in ranges:
            for blob in i.find_all('a'):
                file_name, download_url = self._extract_name_url(blob)
                downloads[file_name] = download_url

        return downloads

    @staticmethod
    def _save_script(content: bytes, file_name: str, path: Union[str, Path]) -> None:
        file_path = path / file_name
        open(file_path, 'wb').write(content)

    @staticmethod
    def _fetch_content(url: str) -> bytes:
        r = requests.get(url)
        if r.status_code != 200:
            r.raise_for_status()
        return r.content

    async def _fetch_and_save(self, session: aiohttp.ClientSession, url: str,
                              file_name: str, path: Union[str, Path],
                              chunk_size: int = 1000) -> None:
        file_path = path / file_name
        async with session.get(url) as resp:
            if resp.status != 200:
                # if resp.status == 404:

                # print(url)
                # resp.raise_for_status()
                return
            with open(file_path, 'wb') as fd:
                while True:
                    chunk = await resp.content.read(chunk_size)
                    if not chunk:
                        break
                    fd.write(chunk)

    def _mkdir(self, folder: Union[str, Path] = None) -> Path:
        pwd = Path('.')
        if folder:
            pwd = pwd / folder / self.series
        else:
            pwd = pwd / self.series
        pwd.mkdir(parents=True, exist_ok=True)

        return pwd

    async def _get_scripts(self, path: Union[str, Path]) -> None:
        tasks = []
        names_with_urls = self._collect_download_names_urls()

        async with aiohttp.ClientSession() as session:
            for file_name, url in names_with_urls.items():
                # pass Semaphore and session to every GET request
                task = asyncio.ensure_future(
                    self._fetch_and_save(session, url, file_name, path)
                )
                tasks.append(task)

            responses = asyncio.gather(*tasks)
            await responses

    def download_scripts(self, folder: Union[str, Path] = None) -> None:
        loop = asyncio.get_event_loop()
        path = self._mkdir(folder)
        print('Downloading...')
        future = loop.create_task(self._get_scripts(path))
        loop.run_until_complete(future)
        print(f'Finished downloading to {path.absolute()}')