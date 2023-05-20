from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db
from . import login_manager

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64), index = True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return f'Id {self.id} name {self.name}'

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id'))
    passwd_hash = db.Column(db.String(255))

    @property
    def password(self):
        raise AttributeError('Password is not reabable or stored')
    
    @password.setter
    def password(self, password):
        self.passwd_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.passwd_hash, password)

    def __repr__(self):
        return f'Id {self.id} username {self.username}'
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))