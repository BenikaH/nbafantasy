import json
import logging
from pprint import pprint
import re

from bs4 import BeautifulSoup as BS

class RotoGrindersNBAParser(object):
    '''
    '''

    def __init__(self):
        '''
        '''
        logging.getLogger(__name__).addHandler(logging.NullHandler())


    def odds(self, content):
        '''
        Gets javascript variable with odds

        Args:
            content: html string

        Returns:
            List of odds
        '''
        patt = re.compile(r'schedules:\s+({.*?}),\s+startedGames', re.MULTILINE | re.DOTALL)
        match = re.search(patt, content)
        if match:
            return match.groups(1)[0]
        else:
            logging.error('no match')
            return None


if __name__ == "__main__":
    pass
