from startrek.episode import Series
from startrek.spider import StarTrekSpider
from imdb import IMDb


class StarTrek:
    _series_short = {'movies', 'ds9', 'tng', 'tos', 'voyager', 'enterprise'}
    _full_name = "Star Trek - {}"
    _series_names = {
        "movies":     "Movies",
        "tng":        "The Next Generation",
        "tos":        "The Original Series",
        "voyager":    "Voyager",
        "ds9":        "Deep Space Nine",
        "enterprise": "Enterprise"
    }
    _movie_names = {}

    def __init__(self, series: str):
        if series not in self._series_short:
            raise ValueError(f'Invalid series {series}. {self._series_short}')
        self._series = series
        self.full_name = self._full_name.format(self._series_names[series])
        self.spider = StarTrekSpider(series=series)
        self.episodes = None

    def __str__(self):
        return self._full_name.format(self._series_names[self._series])

    def __repr__(self):
        return f'<class startrek.StarTrek, series: {self._series_names[self._series]}>'

    @property
    def series(self):
        return self._series

    @series.setter
    def series(self, var):
        if var not in self._series_short:
            raise ValueError(f'Invalid series {var}. {self._series_short}')
        del self.episodes
        self._series = var
        self.full_name = self._full_name.format(self._series_names[var])

    def download_scripts(self, folder=None):
        self.spider.download_scripts(folder)

    def download_imdb_episodes(self):
        if self.episodes:
            return self.episodes

        print('Downloading episodes...')
        ia = IMDb()
        show = ia.search_movie(self.full_name)[0]
        imdbID = ia.get_imdbID(show)
        show = ia.get_movie(imdbID)

        # Gets all episodes Dict[season, list[episodes]]
        ia.update(show, 'episodes')

        self.episodes = Series(show['episodes'])
        print('Finished populating episodes.')

    def get_episode(self, season: int, episode: int):
        return self.episodes.get_episode(season, episode)
