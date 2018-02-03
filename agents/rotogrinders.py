import logging

from nba.parsers.rotogrinders import RotoGrindersNBAParser
from nba.pipelines.nbacom import *
from nba.scrapers.rotogrinders import RotoGrindersNBAScraper


class RotogrindersNBAAgent(object):
    '''
    Performs script-like tasks from rotogrinders
    '''

    def __init__(self, db=None, cache_name='rg-agent', cookies=None, table_names=None):
        '''
        Args:
            db (NBAPostgres): instance
            cache_name (str): for scraper cache_name
            cookies: cookie jar
            table_names (dict): Database table names

        '''
        logging.getLogger(__name__).addHandler(logging.NullHandler())
        self.scraper = RotoGrindersNBAScraper(cache_name=cache_name, cookies=cookies)
        self.parser = RotoGrindersNBAParser()
        self.db = db
        self.table_names = table_names



if __name__ == '__main__':
    pass