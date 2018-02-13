from app import db

db.Model.metadata.reflect(db.engine)


class Player(db.Model):
    __table__ = db.Model.metadata.tables['player']

    def __repr__(self):
        return self.display_first_last

class Playerstats(db.Model):
    __table__ = db.Model.metadata.tables['playerstats_daily']

    def __repr__(self):
        return '{} {}'.format(self.nbacom_player_id, self.player_name)

class Season(db.Model):
    __table__ = db.Model.metadata.tables['season']

    def __repr__(self):
        return '{} {}'.format(self.season_year, self.season_code)
