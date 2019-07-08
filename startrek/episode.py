from imdb.Movie import Movie
from typing import Dict, List, Union, Optional, Sequence
from startrek.script import Script
from startrek.utils import sorted_dict



# TODO: Convert all this to a database

class DictMixin:
    @classmethod
    def from_dict(cls, d: Dict, *, allowed: List[str]):
        df = {k: v for k, v in d.items() if k in allowed}

        return cls(**df)

class IMDbMixin:
    @classmethod
    def from_imdb(cls, imdb_movie: Movie, allowed: Optional[Sequence[str]]=None):
        if not isinstance(imdb_movie, Movie):
            raise ValueError('Invalid IMDb movie format.')

        # df = {}

        # Replace the spaces so the names can be used as dict keys.
        if allowed:
            for key, value in imdb_movie.items():
                if key in allowed or key.replace('_', ' ') in allowed:
                    # df[key.replace(' ', '_')] = value
                    setattr(cls, key.replace(' ', '_'), value)
        else:
            for key, value in imdb_movie.items():
                # df[key.replace(' ', '_')] = value
                setattr(cls, key.replace(' ', '_'), value)

        # Set movieID
        setattr(cls, 'movieID', imdb_movie.movieID)
        # df['movieID'] = imdb_movie.movieID

        return cls

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
            self.episodes[episode_number] = Episode.from_imdb(episode, allowed=Episode.allowed)
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

# @dataclass
class Episode(IMDbMixin):
    allowed = ('rating', 'season', 'episode', 'episode title', 'series title',
               'original air date', 'title', 'votes', 'year', 'movieID')

    def __init__(self, episode: Dict[Union[str, int], Union[str, int, float]], **kwargs) -> None:

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
        return self.title

    def __str__(self):
        return self.title

    def add_script(self, script):
        self.script = Script(script)

    # def from_imdb(self, imdb_movie, allowed: List[str] = None):
    #     if not isinstance(imdb_movie, Movie):
    #         raise ValueError('Invalid IMDb movie format.')
    #
    #     # Replace the spaces so the names can be used as dict keys.
    #     for key in imdb_movie.keys():
    #         # key.replace(' ', '_')
    #         # if allowed:
    #         #     if key in allowed:
    #         #         setattr(cls, key, imdb_movie[key])
    #         # else:
    #         setattr(cls, key.replace(' ', '_'), imdb_movie[key])
    #
    #     return cls

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
