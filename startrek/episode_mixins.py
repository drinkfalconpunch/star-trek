from imdb.Movie import Movie
from typing import Dict

class DictMixin:
    @classmethod
    def from_dict(cls, d: Dict):
        df = {k.replace(' ', '_'): v for k, v in d.items()}

        return cls(df)

class IMDbMixin:
    @classmethod
    def from_imdb(cls, imdb_movie: Movie):
        if not isinstance(imdb_movie, Movie):
            raise ValueError('Invalid IMDb movie format.')

        df = {k.replace(' ', '_'): v for k, v in imdb_movie.items()}
        df['movieID'] = int(str(imdb_movie.movieID).lstrip('0'))

        return cls(df)