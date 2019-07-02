from dataclasses import dataclass
from imdb import Movie

# TODO: Convert all this to a database


class Season:
    pass

class Series:
    '''American version of a TV series consisting of one or more seasons.'''
    pass

# @dataclass
class Episode:
    def __init__(self, imdb_episode, **kwargs) -> None:
        if not isinstance(imdb_episode, Movie.Movie):
            raise ValueError('Invalid IMDb episode format.')
        

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
#         script: str = None

    @property
    def series_sub_title(self) -> str:
        full_title = self.series_full_title()
        if full_title:
            return full_title[11:]
        return None
    
    @property
    def series_full_title(self) -> str:
        try:
            title = getattr(self, 'series_title')
            return title[:-29]
        except AttributeError:
            return None