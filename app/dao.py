from app.models import *
from app import db, app
from flask_login import current_user
from sqlalchemy import func
import hashlib


def get_all_airport():
    return Airport.query.all()


def register(name, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name, username=username, password=password, avatar=avatar)
    db.session.add(u)
    db.session.commit()


def get_flight():
    return Flight.query.all()


def get_user_by_id(user_id):
    return User.query.get(user_id)