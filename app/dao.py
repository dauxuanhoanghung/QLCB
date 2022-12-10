from app.models import *
from app import db, app
from flask_login import current_user
from sqlalchemy import func
import hashlib


def register(name, username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name.strip(),
             username=username.strip(),
             password=password,
             avatar=kwargs.get('avatar'),
             email=kwargs.get('email'),
             phone_number=kwargs.get('phone_number'),
             identity_number=kwargs.get('identity_number'))

    db.session.add(u)
    db.session.commit()


def get_flight():
    return Flight.query.all()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def get_all_airport():
    return Airport.query.all()


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()