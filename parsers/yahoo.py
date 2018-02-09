import logging
import json
from nba.utility import merge_two, merge_many


class YahooNBAParser(object):

    def __init__(self):
        logging.getLogger(__name__).addHandler(logging.NullHandler())

    def teams(self, content):
        '''
        Parses teams API call
        
        Args:
            content (dict): parsed JSON
        
        Returns:
            list: of dict
            
        '''
        results = []
        for k,v in content['fantasy_content']['league'][1]['teams'].items():
            t = []
            if k == 'count':
                continue
            else:
                for item in v['team'][0]:
                    if item:
                        t.append(item)
            results.append(merge_many({}, t))
        return results


if __name__ == '__main__':
    pass
