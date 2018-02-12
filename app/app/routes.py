from string import ascii_uppercase

from flask import render_template, jsonify

from app import app, dates
from app.models import Season, Player


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/seasons', methods=['GET'])
def seasons():
    return render_template('seasons.html', seasons=Season.query.all())

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
    data = [(p.nbacom_player_id, p.first_name, p.last_name, p.nbacom_position, p.primary_position,
             p.position_group, dates.datetostr(p.birthdate, fmt='nba'))
            for p in players]
    return jsonify({'data': data})
