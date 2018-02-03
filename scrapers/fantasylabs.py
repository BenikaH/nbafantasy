import logging

from nba.dates import *
from nba.scrapers.scraper import BasketballScraper


class FantasyLabsNBAScraper(BasketballScraper):
    '''
    Usage:

        s = FantasyLabsNBAScraper()
        games_json = s.today()
        model_json = s.model()
        model_json = s.model('bales')

        for d in date_list('10_09_2015', '10_04_2015'):
            datestr = datetime.strf
            model_json = s.model(model_date=datestr)
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
        self.model_urls = {
            'default': 'https://www.fantasylabs.com/api/playermodel/2/{}/?modelId=193718&projOnly=true',
        }

    def model(self, model_day, model_name='default'):
        '''

        Args:
            model_day (str): in mm_dd_yyyy format
            model_name (str): default, phan, etc.

        Returns:
            dict
        '''
        url = self.model_urls.get(model_name)
        if not url:
            url = self.model_urls.get('default')
        return self.get_json(url=url.format(model_day))

    def models(self, start_date, end_date, model_name='phan'):
        '''
        Gets json for models in date range, default to Phan model
        Stats in most models the same, main difference is the ranking based on weights of factors present in all models

        Usage:
            s = FantasyLabsNBAScraper()
            models = s.models(start_date='10_04_2015', end_date='10_09_2015', model_name='phan')
            
        '''

        if not model_name:
            model_name = self.default_model

        contents = {}

        for d in date_list(end_date, start_date):
            datestr = datetime.datetime.strftime(d, site_format('fl'))
            contents[datestr] = self.model(model_day=datestr, model_name=model_name)

        return contents

    def ownership(self, game_date):
        '''
        Gets ownership percentages
        Args:
            game_date:

        Returns:
            List of percentages
        '''
        # check if game_date in proper format
        base_url = 'http://www.fantasylabs.com/api/contest-ownership/2/{}/4/'
        fmt = convert_format(game_date, 'fl')
        if not fmt:
            raise ValueError('Incorrect date format: {}'.format(game_date))
        else:
            return self.get_json(base_url.format(fmt))


if __name__ == "__main__":
    pass