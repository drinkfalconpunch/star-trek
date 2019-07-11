import logging


class StarTrekException(Exception):
    """Base class exception"""
    _logger = logging.getLogger('startrek')

    def __init__(self, *args, **kwargs):
        """Log exception"""
        self._logger.critical(f'{self.__class__.__name__} exception raised - args: {args}, '
                              f'kwargs: {kwargs}.', exc_info=True)
        super(StarTrekException, self).__init__(*args, **kwargs)

class SpiderException(StarTrekException):
    pass

class ScriptException(StarTrekException):
    pass

class SeriesException(StarTrekException):
    pass