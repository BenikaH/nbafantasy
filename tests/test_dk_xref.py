from __future__ import absolute_import, print_function

import logging
import os
import sys
import unittest

from configparser import ConfigParser

from nba.db.pgsql import NBAPostgres
from nba.names import match_player
from nba.utility import csv_to_dict


class DKxref_test(unittest.TestCase):

    def setUp(self):
        config = ConfigParser()
        config.read(os.path.join(os.path.expanduser('~'), '.pgcred'))
        self.db = NBAPostgres(user=config['nbadb']['username'],
                         password=config['nbadb']['password'],
                         database=config['nbadb']['database'])


    def test_xref(self):
        q = """SELECT nbacom_player_id, display_first_last FROM players
               WHERE nbacom_player_id IN
               (SELECT DISTINCT nbacom_player_id FROM player_gamelogs WHERE game_date > '2014-10-01')
               """
        players = {p['display_first_last']:p['nbacom_player_id'] for p in self.db.select_dict(q)}
        dkp = list(csv_to_dict('/home/sansbacon/dkxref.csv'))
        for idx, p in enumerate(dkp):
            nm = match_player(p['source_player_name'], players.keys())
            pid = players.get(nm)
            if pid:
                dkp[idx]['nbacom_player_id'] = pid
                self.db._insert_dict(dkp[idx], 'player_xref')
            else:
                logging.info('no match for {}'.format(p))


if __name__=='__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    unittest.main()