import base64
import datetime
import json
import logging
import webbrowser


from nbafantasy.scrapers.scraper import BasketballScraper
from nbafantasy.utility import merge_two


class YahooFantasyScraper(BasketballScraper):

    def __init__(self, authfn, yahoo_season=None, sport='nba',
                 headers=None, cookies=None, cache_name=None, expire_hours=4, as_string=False):
        '''
        Initialize scraper object

        Args:
            authfn (str): path of auth.json file
            yahoo_season (int): default current season
            sport (str): default 'nba'
            headers (dict): dict of headers
            cookies (obj): cookies object
            cache_name (str): 
            expire_hours (int): hours to keep in cache
            as_string (bool): false -> returns parsed json, true -> returns string

        Returns:
            YahooFantasyScraper

        '''
        logging.getLogger(__name__).addHandler(logging.NullHandler())
        BasketballScraper.__init__(self, headers=headers, cookies=cookies, cache_name=cache_name,
                                   expire_hours=expire_hours, as_string=as_string)
        self.authfn = authfn
        if not yahoo_season:
            d = datetime.datetime.now()
            y = d.year
            m = d.month
            if m >= 9:
                self.yahoo_season = y
            else:
                self.yahoo_season = y - 1
        else:
            self.yahoo_season = yahoo_season

        self.sport = sport
        self.token_uri = 'https://api.login.yahoo.com/oauth2/get_token'
        self.auth_uri = 'https://api.login.yahoo.com/oauth2/request_auth'

        # load credentials
        with open(self.authfn) as infile:
            self.auth = json.load(infile)

        # check file for refresh token
        if self.auth.get('refresh_token'):
            self.refresh_credentials()

        # if don't have a refresh token, then request auth
        else:
            params = {'client_id': self.auth['client_id'],
                      'redirect_uri': 'oob',
                      'response_type': 'code',
                      'language': 'en-us'}
            r = self.s.get(self.auth['auth_uri'], params=params)

            # response url will allow you to plug in code
            i = 1
            while i:
                # you may need to add export BROWSER=google-chrome to .bashrc
                webbrowser.open(url=r.url)
                code = input('Enter code from url: ')
                i = 0

            # now get authorization token
            hdr = self.auth_header
            body = {'grant_type': 'authorization_code', 'redirect_uri': 'oob', 'code': code}
            headers = {'Authorization': hdr,
                       'Content-Type': 'application/x-www-form-urlencoded'}
            r = self.s.post(self.token_uri, data=body, headers=headers)

            # add the token to auth
            self.auth = merge_two(self.auth, r.json())

            # now write back to file
            with open(self.authfn, 'w') as outfile:
                json.dump(self.auth, outfile)

    @property
    def auth_header(self):
        '''
        Basic authorization header
        
        Args:
            None
            
        Returns:
            str

        '''
        string = '%s:%s' % (self.auth['client_id'], self.auth['client_secret'])
        base64string = base64.standard_b64encode(string.encode('utf-8'))
        return "Basic %s" % base64string.decode('utf-8')

    @property
    def game_key(self):
        '''
        Game key for queries

        '''
        if self.sport == 'nba':
            return {2017: 375}.get(self.yahoo_season)
        else:
            return None

    def game(self):
        '''
        Gets game resource
        
        Args:
            None
                        
        Returns:
            dict: parsed json
            
        '''
        url = 'https://fantasysports.yahooapis.com/fantasy/v2/game/{}'
        return self.query(url.format(self.sport))

    def league(self, league_id, subresource='metadata'):
        '''
        Gets league resource

        Args:
            league_id (int): id for your league
            subresource (str): metadata, settings, standings, scoreboard, etc.

        Returns:
            dict: parsed json

        '''
        if subresource not in ['metadata', 'settings', 'standings', 'scoreboard']:
            raise ValueError('invalid subresource')

        param = '{}.l.{}'.format(self.game_key(self.yahoo_season), league_id)
        url = 'https://fantasysports.yahooapis.com/fantasy/v2/league/{}/{}'
        return self.query(url.format(param), subresource)

    def players(self, league_id, filters=None):
        '''
        Gets league resource

        Args:
            league_id (int): id for your league
            kwargs

        Returns:
            dict: parsed json

        '''
        # deal with kwargs here

        #url = 'https://fantasysports.yahooapis.com/fantasy/v2/players'
        #return self.query(url.format(param))

    def league_key(self, league_id):
        '''
        League key given league_id
        
        Args:
            league_id (int): 

        Returns:
            str
        '''
        return '{}.l.{}'.format(self.game_key, league_id)

    def query(self, url, params={'format': 'json'}):
        '''
        Query yahoo API
               
        '''
        hdr = {'Authorization': 'Bearer %s' % self.auth['access_token']}
        if params:
            r = self.s.get(url, headers=hdr, params=params)
        else:
            r = self.s.get(url, headers=hdr)
        content = r.json()
        if 'error' in content:
            # if get error for valid credentials, refresh and try again
            desc = content['error']['description']
            if 'Please provide valid credentials' in desc:
                self.refresh_credentials()
                if params:
                    r = self.s.get(url, headers=hdr, params=params)
                else:
                    r = self.s.get(url, headers=hdr)
        return r.json()

    def refresh_credentials(self):
        '''
        Refreshes yahoo token
        
        Returns:
            None
            
        '''
        body = {'grant_type': 'refresh_token', 'redirect_uri': 'oob', 'refresh_token': self.auth['refresh_token']}
        headers = {'Authorization': self.auth_header,
                   'Content-Type': 'application/x-www-form-urlencoded'}
        r = self.s.post(self.token_uri, data=body, headers=headers)

        # add the token to auth
        self.auth = merge_two(self.auth, r.json())

        # now write back to file
        with open(self.authfn, 'w') as outfile:
            json.dump(self.auth, outfile)

    def teams(self, league_id, subresource=None):
        '''
        Gets teams resource

        Args:
            league_id (int): id for your league
            subresource (str):

        Returns:
            dict: parsed json

        '''
        url = 'http://fantasysports.yahooapis.com/fantasy/v2/league/{league_key}/teams'
        return self.query(url.format(league_key=self.league_key(league_id)))


if __name__ == '__main__':
    pass
