# donbest.py
# pipeline from scraped data to other formats

from copy import deepcopy
from nba.dates import convert_format
from nba.teams import long_to_code


def game_odds(odds):
    newodds = []
    for o in odds:
        fixed = {}
        fixed['away'] = long_to_code(o.get('away'))
        fixed['home'] = long_to_code(o.get('home'))
        try:
            fixed['consensus_spread'] = float(o.get('consensus_spread'))
            fixed['consensus_game_ou'] = float(o.get('consensus_total'))
        except:
            pass
        fixed['opening_spread'] = o.get('opening_spread')
        fixed['opening_game_ou'] = o.get('opening_game_ou')
        fixed['gamecode'] = '{}/{}{}'.format(o.get('game_date'), fixed['away'], fixed['home'])
        fixed['game_date'] = convert_format(o.get('game_date'), 'nba')
        newodds.append(fixed)

    for newo in newodds:
        t1 = deepcopy(newo)
        t1['team_code'] = newo['away']
        t1.pop('away', None)
        t1.pop('home', None)
        t1['opening_spread'] = 0 - t1['opening_spread']
        t1['consensus_spread'] = 0 - t1['consensus_spread']
        t2 = deepcopy(newo)
        t2['team_code'] = newo['home']
        t2.pop('away', None)
        t2.pop('home', None)

    return newodds