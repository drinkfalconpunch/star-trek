from imdb.Movie import Movie
from typing import Dict, Union
from startrek.script import Script
from startrek.utils import sorted_dict
from startrek.episode_mixins import IMDbMixin


# TODO: Convert all this to a database

class Season:
    def __init__(self, season_number: int, episodes: Dict[int, Movie]):
        self.season = season_number
        self._episodes = episodes
        self.episodes = {}
        self._populate_episodes()

    def get_episode(self, episode):
        try:
            return self.episodes[episode]
        except KeyError:
            print(f'Invalid episode {episode}.')

    def _populate_episodes(self):
        for episode_number, episode in self._episodes.items():
            self.episodes[episode_number] = Episode.from_imdb(episode)
        self.episodes = sorted_dict(self.episodes)
        del self._episodes


class Series:
    '''American version of a TV series consisting of one or more seasons.'''

    def __init__(self, seasons: Dict[int, Dict[int, Movie]] = None):
        self._seasons = seasons
        self.seasons = {}
        self._populate_seasons()

    def _populate_seasons(self):
        for season_number, episodes in self._seasons.items():
            self.seasons[season_number] = Season(season_number, episodes)
        self.seasons = sorted_dict(self.seasons)
        del self._seasons

    def get_season(self, season_number):
        try:
            return self.seasons[season_number]
        except KeyError:
            print(f'Invalid season {season_number}.')

    def get_episode(self, season_number, episode_number):
        season = self.get_season(season_number)
        return season.get_episode(episode_number)


class Episode(IMDbMixin):
    def __init__(self, episode: Dict[Union[str, int], Union[str, int, float]], **kwargs) -> None:
        self.allowed = ('rating', 'season', 'episode', 'episode title', 'series title',
                        'original air date', 'title', 'votes', 'year', 'movieID')

        # Replace the spaces so the names can be used as dict keys.
        for key, value in episode.items():
            if key in self.allowed or key.replace('_', ' ') in self.allowed:
                setattr(self, key.replace(' ', '_'), value)

        # Initialize any extra values
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.script = None

        del self.allowed

    def __repr__(self):
        return getattr(self, 'title', '')

    def __str__(self):
        return getattr(self, 'title', '')

    def add_script(self, script):
        self.script = Script(script)

    @property
    def series_sub_title(self) -> str:
        full_title = self.series_full_title
        if full_title:
            return full_title[11:]
        return ''

    @property
    def series_full_title(self) -> str:
        try:
            title = getattr(self, 'series_title')
            return title[:-29]
        except AttributeError:
            return ''

    def set_script(self, script_path=None, script_text=None):
        if script_path:
            script_text = open(script_path, 'r').read()
        else:
            if not script_text:
                script_text = ''
        self.script = Script(script_text, series_name=self.series_title,
                                 season_number=self.season, episode_number=self.episode)