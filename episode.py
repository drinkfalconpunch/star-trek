from dataclasses import dataclass
from imdb import Movie.Movie
from typing import Dict
from script import Script


# TODO: Convert all this to a database


class Season:
    def __init__(self, season: int, episodes):
        self.season = season
        self.episodes = {}



class Series:
    '''American version of a TV series consisting of one or more seasons.'''
    def __init__(self, episodes: Dict[int, Dict[int, Movie.Movie]] = None):
        self.episodes = episodes
        self.seasons = {}
        self._populate_seasons()

    def _populate_seasons(self):
        for _season, _episodes in self.episodes.items():
            self.seasons[_season] = _episodes
        del self.episodes

    def get_season(self, season):
        try:
            return self.seasons[season]
        except:
            raise KeyError(f'Invalid season {season}.')

    def get_episode(self, season, episode):
        try:
            return self.get_season(season)[episode]
        except:
            raise KeyError(f'Invalid episode {episode}.')

# @dataclass
class Episode:
    def __init__(self, imdb_episode: Movie.Movie, **kwargs) -> None:
        if not isinstance(imdb_episode, Movie.Movie):
            raise ValueError('Invalid IMDb episode format.')

        # Replace the spaces so the names can be used as dict keys.
        for key in imdb_episode.keys():
            setattr(self, key.replace(' ', '_'), imdb_episode[key])

        # Initialize any extra values
        for key in kwargs:
            setattr(self, key, kwargs[key])

    #         _series_name: str = ''
    #         season_number: int = 0
    #         episode_number: int = 0
    #         episode_name: str = ''
    #         alt_name: str = ''
    #         multi_part: bool = False
    #         script_file_type: str = ''
        self.script = None

    def __repr__(self):
        return ''

    def __str__(self):
        return ''

    @property
    def series_sub_title(self) -> str:
        full_title = self.series_full_title()
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
