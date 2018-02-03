"""
# pipelines/rotoguru.py
# functions to transform rotoguru data
# for insertion into database, use in optimizer, etc.
"""

from __future__ import print_function
import logging

from nameparser import HumanName
from pydfs_lineup_optimizer.player import Player


logging.getLogger(__name__).addHandler(logging.NullHandler())


def rotoguru_make_player(p):
    '''

    Args:
        p:

    Returns:
        Player
    '''
    hn = HumanName(p.get('name'))
    return Player(
        p.get('id'),
        hn.first,
        hn.last,
        [p.get('position')],
        p.get('team'),
        int(p.get('salary', 0)),
        float(p.get('pts', 0))
    )


def rotoguru_to_pydfs(players):
    '''
    Makes results ready to create Player objects for pydfs_lineup_optimizer

    Args:
        players: list of dict

    Returns:
        players (list): list of Player objects for use in pydfs_lineup_optimizer
    '''
    return [rotoguru_make_player(p) for p in players]


if __name__ == '__main__':
    pass