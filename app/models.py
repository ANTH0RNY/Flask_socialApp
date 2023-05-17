from . import db

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64), index = True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return f'Id {self.id} name {self.name}'

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(64), index=True)
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id'))

    def __repr__(self):
        return f'Id {self.id} username {self.username}'
