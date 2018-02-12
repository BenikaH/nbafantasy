from app import db

db.Model.metadata.reflect(db.engine)


class Player(db.Model):
    __table__ = db.Model.metadata.tables['player']

    def __repr__(self):
        return self.display_first_last


class Season(db.Model):
    __table__ = db.Model.metadata.tables['season']

    def __repr__(self):
        return '{} {}'.format(self.season_year, self.season_code)
