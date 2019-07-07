import re
from pathlib import Path

from episode import Episode, Season, Series
from spider import StarTrekSpider
from imdb import IMDb
from imdb.helpers import sortedSeasons, sortedEpisodes




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
        self.episodes = []
        self._episodes = None

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
        self._series = var
        self.full_name = self._full_name.format(self._series_names[var])

    def download_scripts(self, folder=None):
        self.spider.download_scripts(folder)

    def _get_series(self):
        if self._episodes:
            return self._episodes

        ia = IMDb()
        show = ia.search_movie(self.full_name)[0]
        imdbID = ia.get_imdbID(show)
        show = ia.get_movie(imdbID)

        # Gets all episodes Dict[season, list[episodes]]
        ia.update(show, 'episodes')

        self._episodes = Series(show['episodes'])

    def get_episode(self, season: int, episode: int):


        Episode(imdb_episode=episode)

        for season, episodes in show['episodes'].items():


        return episodes

    def _populate_episodes(self):
        # r = requests.get(self._url_base.format(self.series))
        # soup = BeautifulSoup(r.content, 'lxml')

        episode_name_regex = (
            r"(?<=\-\s).*(?=\.txt)"
        )  # (?<=\-\s) matches after '- ', (?=\.) matches before '.',
        # and '.*' is everything inside.
        original_name_regex = (
            r"^(.+?)\saka*"
        )  # matches everything from the beginning of the string to ' aka'
        alt_name_regex = (
            r"(?<=aka\s).*$"
        )  # matches everything after 'aka ' to the end of the string if it exists.

        episode_pattern = re.compile(episode_name_regex)
        original_name_pattern = re.compile(original_name_regex)
        alt_name_pattern = re.compile(alt_name_regex)

        for s in soup.find_all("a", class_=self._classes[self.series]):
            episode = Episode()
            episode.series_name = self._series_names[self.series]
            content = s.contents[0][
                      len(self._full_name.format(self._series_names[self.series])) + 1:
                      ]  # cause googling how to get after the second - is not working atm
            episode_name = re.findall(
                episode_pattern, content
            )  # s.contents[0][len(_full_name.format(_series_names['tng']))+1:])
            if episode_name:
                alt_name = re.findall(alt_name_pattern, episode_name[0])
                try:
                    episode.episode_name = episode_name[0].split(" aka")[0]
                except KeyError:
                    pass
                if alt_name:
                    episode.alt_name = alt_name[0]
                episode.script_file_type = Path(content).suffix[1:]
                episode.season_number = content[0]
                episode.episode_number = content[2:4]
            self.episodes.append(episode)