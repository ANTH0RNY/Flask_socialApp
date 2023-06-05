from functools import wraps
from flask import abort
from flask_login import current_user
from .models import  Permissions

def perimssion_required(permission):
    def decorator(func):
        @wraps(fun)
        def function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return func(*args, **kwargs)
        return function
    return decorator

def admin(func):
    return perimssion_required(Permissions.ADMIN)

def moderator(func):
    return perimssion_required(Permissions.MODERATE)