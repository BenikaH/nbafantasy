import logging

from nba.dates import *
from nba.scrapers.scraper import BasketballScraper


class RotoGrindersNBAScraper(BasketballScraper):
    '''
    '''

    def __init__(self, headers=None, cookies=None, cache_name=None, expire_hours=4, as_string=False):
        '''
        Initialize scraper object

        Args:
            headers: dict of headers
            cookies: cookies object
            cache_name: str
            expire_hours: int hours to keep in cache
            as_string: bool, false -> returns parsed json, true -> returns string

        Returns:
            scraper object
        '''
        logging.getLogger(__name__).addHandler(logging.NullHandler())
        BasketballScraper.__init__(self, headers=headers, cookies=cookies, cache_name=cache_name,
                                   expire_hours=expire_hours, as_string=as_string)


    def odds(self):
        '''
        Gets odds from today

        Returns:
            html string
        '''
        url = 'https://rotogrinders.com/schedules/nba'
        return self.get(url)


if __name__ == "__main__":
    pass