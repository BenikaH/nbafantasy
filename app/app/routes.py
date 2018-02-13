import logging
from string import ascii_uppercase

from flask import render_template, jsonify

from app import app, dates, db
from app.models import Season, Player, Playerstats


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/seasons', methods=['GET'])
def seasons():
    return render_template('seasons.html', seasons=Season.query.all())


@app.route('/player/<player_id>', methods=['GET'])
def player(player_id):
    logging.debug(player_id)
    tbl_headers = ['Season', 'Date', 'Player', 'Team', 'Fantasy Points']
    return render_template('player.html', headers=tbl_headers, player_id=player_id)


@app.route('/players', methods=['GET'])
def players():
    tbl_headers = ['NBA.com ID', 'First Name', 'Last Name', 'NBA.com Pos', 'Primary Pos', 'Pos Group', 'DOB']
    letters = [l for l in ascii_uppercase if l != 'X']
    return render_template('players.html', headers=tbl_headers, letters=letters)


@app.route('/players_ajax/<last>', methods=['GET'])
def players_ajax_last(last):
    if last == 'All' or not last:
        players = Player.query
    elif last:
        players = Player.query.filter(Player.last_name.like('{}%'.format(last)))
    data = [('<a href="/player/{0}">{0}</a>'.format(p.nbacom_player_id), p.first_name, p.last_name,
             p.nbacom_position, p.primary_position,
             p.position_group, dates.datetostr(p.birthdate, fmt='nba'))
            for p in players]
    return jsonify({'data': data})


@app.route('/player_ajax/<player_id>', methods=['GET'])
def player_ajax_pid(player_id):
    q = ("""SELECT season_year, as_of, player_name, team_code, nba_fantasy_pts """
         """FROM playerstats_daily WHERE nbacom_player_id = {} AND per_mode = 'Totals' """
         """ORDER BY as_of DESC LIMIT 10""").format(player_id)
    logging.info(q)
    data = [(p.season_year, dates.datetostr(p.as_of, fmt='nba'), p.player_name, p.team_code, p.nba_fantasy_pts)
            for p in db.engine.execute(q)]
    return jsonify({'data': data})