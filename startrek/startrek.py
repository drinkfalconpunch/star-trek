from startrek.episode import Series
from startrek.spider import StarTrekSpider
from imdb import IMDb


class StarTrek:
    _star_trek = {
        "Movies": {
            "short_name": ["movies"],
            "imdb_movie_number": 0
        },
        "The Next Generation": {
            "short_name": ["tng"],
            "imdb_movie_number": 92455
        },
        "The Original Series": {
            "short_name": ["tos"],
            "imdb_movie_number": 60028
        },
        "Voyager": {
            "short_name": ["voyager"],
            "imdb_movie_number": 112178
        },
        "Enterprise": {
            "short_name": ["enterprise"],
            "imdb_movie_number": 244365
        },
        "Deep Space Nine": {
            "short_name": ["ds9"],
            "imdb_movie_number": 106145
        }
    }
    _series_short_names = {'movies', 'ds9', 'tng', 'tos', 'voyager', 'enterprise'}
    _full_name = "Star Trek - {}"
    _series_long_names = {
        "movies":     "Movies",
        "tng":        "The Next Generation",
        "tos":        "The Original Series",
        "voyager":    "Voyager",
        "ds9":        "Deep Space Nine",
        "enterprise": "Enterprise"
    }
    _movie_names = {}

    def __init__(self, series_short_name: str):
        if series_short_name not in self._series_short_names:
            raise ValueError(f'Invalid series {series_short_name}. {self._series_short_names}')
        self._series_short_name = series_short_name
        self.full_name = self._full_name.format(self._series_long_names[self.series_short_name])
        self.spider = StarTrekSpider(series=series_short_name)
        self.series = None

    def __str__(self):
        return self._full_name.format(self._series_long_names[self.series_short_name])

    def __repr__(self):
        return f'<class startrek.StarTrek, series: {self._series_long_names[self.series_short_name]}>'

    @property
    def series_short_name(self):
        return self._series_short_name

    @series_short_name.setter
    def series_short_name(self, var):
        if var not in self._series_short_names:
            raise ValueError(f'Invalid series {var}. {self._series_short_names}')
        del self.series
        self._series_short_name = var
        self.full_name = self._full_name.format(self._series_long_names[var])

    def download_scripts(self, folder=None):
        self.spider.download_scripts(folder)

    def download_imdb_episodes(self):
        if self.series:
            return self.series

        print('Downloading episodes...')
        ia = IMDb()
        # show = ia.search_movie(self.full_name)[0]
        # imdbID = ia.get_imdbID(show)
        long_name = self._series_long_names[self._series_short_name]
        imdbID = self._star_trek[long_name]['imdb_movie_number']
        show = ia.get_movie(imdbID)

        # Gets all episodes Dict[season, list[episodes]]
        ia.update(show, 'episodes')

        self.series = Series(show['episodes'])
        print('Finished populating episodes.')

    def get_episode(self, season: int, episode: int):
        return self.series.get_episode(season, episode)

    def set_script(self, season, episode, script_path=None, script_text=None):
        if not self.series:
            print('Episodes not populated. Use download_imdb_episodes() first.')
            return
        self.series.seasons[season].episodes[episode].set_script(script_path, script_text)
