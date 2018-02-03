from __future__ import absolute_import, print_function

import logging
import os
import sys
import time
import unittest

from configparser import ConfigParser

from nba.agents.rotoguru import RotoGuruNBAAgent
from nba.db.pgsql import NBAPostgres


class RotoGuruNBAAgent_test(unittest.TestCase):

    def setUp(self):
        config = ConfigParser()
        config.read(os.path.join(os.path.expanduser('~'), '.pgcred'))
        db = NBAPostgres(user=config['nbadb']['username'],
                         password=config['nbadb']['password'],
                         database=config['nbadb']['database'])
        self.a = RotoGuruNBAAgent(cache_name='test-rg', db=db)
        self.a.insert_db = False


    def test_salaries_oneday(self):
        d = '20170321'
        sals = self.a.salaries(d)
        self.assertIsNotNone(sals)
        self.assertTrue(len(sals) > 0)


    def test_salaries_all(self):
        sals = self.a.salaries(all_missing=True)
        self.assertIsNotNone(sals)
        self.assertTrue(len(sals) > 0)


if __name__=='__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    unittest.main()
