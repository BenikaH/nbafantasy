"""
# pipelines/fantasylabs.py
# functions to transform fantasylabs data
# for insertion into database, use in optimizer, etc.
"""

from __future__ import print_function
import logging

from nba.seasons import in_what_season
from pydfs_lineup_optimizer.player import Player


logging.getLogger(__name__).addHandler(logging.NullHandler())


def fl_make_player(p, weights=[.6, .3, .1]):
    name = p.get('Player_Name')
    if name and ' ' in name:
        first, last = name.split(' ')[0:2]
    else:
        first = name
        last = None
    mean = p.get('AvgPts')
    floor = p.get('Floor')
    ceiling = p.get('Ceiling')
    fppg = round((mean * weights[0] + ceiling * weights[1] + floor * weights[2]) / sum(weights), 2)

    return Player(
        '',
        first,
        last,
        p.get('Position').split('/'),
        p.get('Team'),
        float(p.get('Salary', 0)),
        fppg
    )


def fl_to_pydfs(models, weights=[.6, .3, .1]):
    '''
    Takes fantasylabs models, make ready to create Player objects for pydfs_lineup_optimizer

    Args:
        models (list): is parsed json from day's models

    Returns:
        players (list): list of players, fixed for use in pydfs_lineup_optimizer

    Examples:
        a = FantasyLabsNBAAgent()
        models = a.today_models()
        players = a.optimizer_pipeline(models)

    '''
    fl_keys = ['PlayerId', 'Player_Name', 'Position', 'Team', 'Salary', 'Score', 'AvgPts', 'Ceiling', 'Floor',
               'ProjPlusMinus']
    fl_players = [{k: v for k, v in p.items() if k in fl_keys} for p in models]

    # remove null values
    for idx, flp in enumerate(fl_players):
        if flp.get('Ceiling') is None:
            fl_players[idx]['Ceiling'] = 0
        if flp.get('Floor') is None:
            fl_players[idx]['Floor'] = 0
        if flp.get('AvgPts') is None:
            fl_players[idx]['AvgPts'] = 0

    return [fl_make_player(p, weights) for p in fl_players]


def salaries_table(sals, game_date):
    '''
    Transforms salary data into dict to insert into table
    Args:
        sals:
        all_players:
        game_date:

    Returns:
        List of dict to insert into db
    '''
    for idx, salary in enumerate(sals):
        fx = {'source': 'fantasylabs', 'dfs_site': 'dk', 'game_date': game_date}
        fx['season'] = in_what_season(game_date, fmt=True)
        fx['source_player_id'] = salary.get('PlayerId')
        fx['source_player_name'] = salary.get('Player_Name')
        fx['salary'] = salary.get('Salary')
        fx['team_code'] = salary.get('Team')
        fx['dfs_position'] = salary.get('Position')
        sals[idx] = fx
    return sals


if __name__ == '__main__':
    pass