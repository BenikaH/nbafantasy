def nba_to_pydfs(players):
    '''
    Takes results, make ready to create Player objects for pydfs_lineup_optimizer

    Args:
        players (list): day's worth of stats

    Returns:
        players (list): list of players, fixed for use in pydfs_lineup_optimizer
    '''
    try:
        from pydfs_lineup_optimizer import Player
        return [Player(p['nbacom_player_id'], p['first_name'], p['last_name'],
                p.get('dfs_position').split('/'),
                p.get('team_code'),
                float(p.get('salary', 100000)),
                float(p.get('dk_points',0))) for p in players]

    except ImportError:
        logging.exception('could not import pydfs_lineup_optimizer')

