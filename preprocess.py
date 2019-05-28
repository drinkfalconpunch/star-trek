import os
from pathlib import Path
import re
import requests
import selenium
from bs4 import BeautifulSoup

from episode import Episode

class StarTrekPreprocessing():
    url_base = 'https://sites.google.com/site/tvwriting/us-drama/show-collections/star-trek-{}'
    _series = set(['tng', 'tos', 'ds9', 'voyager', 'enterprise'])
    
    _classes = {'tng': 'dhtgD'}
    _full_name = 'Star Trek - {}'
    _series_names = {'tng': 'The Next Generation', 'tos': 'The Original Series', 'voy': 'Voyager', 'ds9': 'Deep Space Nine'}
    
    def __init__(self, series='tng', url=None):
        if series not in self._series:
            raise ValueError(f'Invalid series {series}.')
        self.series = series
        self.url = url
        self.episodes = []
    
    def _populate_episodes(self):
        r = requests.get(self.url_base.format(self.series))
        soup = BeautifulSoup(r.content, 'lxml')

        episode_name_regex = r"(?<=\-\s).*(?=\.)" # (?<=\-\s) matches after '- ', (?=\.) matches before '.', and '.*' is everything inside.
        original_name_regex = r"^(.+?)\saka*"
        alt_name_regex = r"(?<=aka\s).*$"

        episode_pattern = re.compile(episode_name_regex)
        original_name_pattern = re.compile(original_name_regex)
        alt_name_pattern = re.compile(alt_name_regex)

        for s in soup.find_all('a', class_=self._classes[self.series]):
            episode = Episode()
            episode.series_name = self._series_names[self.series]
            content = s.contents[0][len(self._full_name.format(self._series_names[self.series]))+1:] # cause googling how to get after the second - is not working atm
            episode_name = re.findall(episode_pattern, content) #s.contents[0][len(_full_name.format(_series_names['tng']))+1:])
            if episode_name:
                alt_name = re.findall(alt_name_pattern, episode_name[0])
                try:
                    episode.episode_name = episode_name[0].split(' aka')[0]
                except KeyError:
                    pass
                if alt_name:
                    episode.alt_name = alt_name[0]
                episode.script_file_type = Path(content).suffix[1:]
                episode.season_number = content[0]
                episode.episode_number = content[2:4]
            self.episodes.append(episode)