from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from . import db
from . import login_manager

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64), index = True)
    users = db.relationship('User', backref='role', lazy='dynamic')
    default = db.Column(db.Boolean, default=False, index=True)
    permission = db.Column(db.Integer)

    def __init__(self, **kwargs):
        super(Role,self).__init__(**kwargs)
        if self.permission is None:
            self.permission = 0
    def __repr__(self):
        return f'Id {self.id} name {self.name}'
    
    def has_permission(self, permission):
        return self.permission & permission == permission

    def add_permission(self, permission):
        if not self.has_permission(permission):
            self.permission += permission
    
    def remove_permission(self, permission):
        if self.permission(permission):
            self.permission -= permission
    
    def reset_permission(self):
        self.permission = 0
    
    @staticmethod
    def insert_roles():
        roles = {
            'User':[Permissions.FOLLOW, Permissions.COMMENT, Permissions.WRITE],
            'Moderator': [Permissions.FOLLOW, Permissions.COMMENT, Permissions.WRITE, Permissions.MODERATE],
            'Admin': [Permissions.FOLLOW, Permissions.COMMENT, Permissions.WRITE, Permissions.MODERATE, Permissions.ADMIN]
        }
        default_role = 'User'
        for i in roles:
            role = Role.query.filter_by(name=i).first()
            if role is None:
                role = Role(name=i)
            role.reset_permission()
            for j in roles[i]:
                role.add_permission(j)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

class Permissions:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id'))
    passwd_hash = db.Column(db.String(255))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            self.role = Role.query.filter_by(default=True).first()

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
    
    def can(self, permission):
        return self.role is not self.role.has_permission(permission)
    
    def is_admin(self):
        return self.can(Permissions.ADMIN)
    
def AnonymousUser(AnonymousUserMixin):
    def can(self, permission):
        return False

    def is_admin(self):
        return False
    
login_manager.anonymous_user = AnonymousUser