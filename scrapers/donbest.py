'''
DonBestNBAScraper
'''

import logging

from nba.dates import *
from nba.scrapers.scraper import BasketballScraper


class DonBestNBAScraper(BasketballScraper):
    '''

    '''

    def __init__(self, headers=None, cookies=None, cache_name=None, expire_hours=4, as_string=False):
        logging.getLogger(__name__).addHandler(logging.NullHandler())
        BasketballScraper.__init__(self, headers=headers, cookies=cookies,
                                   cache_name=cache_name, expire_hours=expire_hours, as_string=as_string)

    def odds(self, day):
        '''
        Odds for NBA game from a single day

        Arguments:
            day: str 20170216

        Returns:
            list of dict
        '''
        base_url = 'http://www.donbest.com/nba/odds/{}.html'
        return self.get(base_url.format(day))


if __name__ == "__main__":
    pass
