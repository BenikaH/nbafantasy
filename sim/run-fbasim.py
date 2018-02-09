'''
run-fbasim.py
'''
import click
import pandas as pd

from nbafantasy.sim.fbasim import load_data, sim, parallelsim


@click.command()
@click.option('--n', default=500, type=int, help='Number of Teams')
@click.option('--league_type', default='Tim', type=str, help='Tim, 8Cat, 9Cat')
@click.option('--thresh_min', default=0, type=int, help='Minimum minutes played')
@click.option('--thresh_gp', default=0, type=int, help='Minimum minutes played')
@click.option('--last_n', default=0, type=int, help='Last Number of Games')
@click.option('--per_mode', default='Totals', type=str, help='Totals, PerGame, Per48')
@click.option('--playerpool_size', default=200, type=int, help='Number of players in pool')
@click.option('--numteams', default=10, type=int, help='Number of teams in league')
@click.option('--sizeteams', default=10, type=int, help='Number of players on team')
@click.option('--parallel', default=0, type=int, help='Use parallel processing')
@click.option('--vorp', default=0, type=int, help='Compare to league average')
def run(n, league_type, thresh_min, thresh_gp, last_n, per_mode, playerpool_size,
        numteams, sizeteams, parallel, vorp):
    '''
    \b
    run-fbasim.py --n=25000 --per_mode='PerGame' --parallel=4 --league_type='8Cat' --vorp
    run-fbasim.py --n=25000 --per_mode='Totals' --league_type='9Cat'
    run-fbasim.py --n=25000 --per_mode='Per48' --league_type='Tim' --thresh_min=500

    '''
    # display sim results
    if league_type == '8Cat':
        initialcols = ['PLAYER_ID', 'FGM', 'FGA', 'FTM', 'FTA', 'FG3M', 
                       'REB', 'AST', 'STL', 'BLK', 'PTS']
        rk_cols = ['FGP_RK', 'FTP_RK', 'FG3M_RK', 'REB_RK', 'AST_RK', 
                   'STL_RK', 'BLK_RK', 'PTS_RK', 'TOT_RK']
    elif league_type == '9Cat':
        initialcols = ['PLAYER_ID', 'FGM', 'FGA', 'FTM', 'FTA', 'FG3M', 
                       'REB', 'AST', 'STL', 'BLK', 'TOV', 'PTS']
        rk_cols = ['FGP_RK', 'FTP_RK', 'FG3M_RK', 'REB_RK', 'AST_RK', 
                   'STL_RK', 'BLK_RK', 'TOV_RK', 'PTS_RK', 'TOT_RK']
    else:
        initialcols = ['PLAYER_ID', 'FGM', 'FGA', 'FTM', 'FG3M', 'REB', 
                       'AST', 'STL', 'BLK', 'TOV', 'PTS']
        rk_cols = ['FGP_RK', 'FTM_RK', 'FG3M_RK', 'REB_RK', 'AST_RK', 
                   'STL_RK', 'BLK_RK', 'TOV_RK', 'PTS_RK', 'TOT_RK']

    players = load_data(per_mode, playerpool_size, thresh_gp, thresh_min, last_n)

    if parallel:
        results = parallelsim(players, initialcols, n, parallel, 
                              numteams, sizeteams)                             
    else:
        results = sim(players, initialcols, n, numteams, sizeteams)
    
    displaycol = ['PLAYER_NAME', 'TEAM', 'GP', 'MIN'] + rk_cols
    if vorp:
        colavg = float((numteams+1)/2)
        for col in rk_cols:
            if col == 'TOT_RK':
                results[col] = results[col] - (len(rk_cols)-1)*colavg               
            else:
                results[col] = results[col] - colavg
    
    pd.set_option('display.width', 1200)
    print(results[displaycol])
    

if __name__ == '__main__':
    run()
