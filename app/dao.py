from app.models import *
from app import db, app
from flask_login import current_user
from sqlalchemy import func
import hashlib


def get_all_ticket_type():
    return TicketType.query.all()


def get_flight(from_airport=None, to_airport=None, start_day=None):
    query = db.session.query(Flight.id, FlightRoute.arrival_airport_id,
                             FlightRoute.departure_airport_id)\
                            .join(FlightRoute, Flight.flight_route_id.__eq__(FlightRoute.id))
    if from_airport:
        query = query.filter(FlightRoute.departure_airport_id.__eq__(from_airport))
    if to_airport:
        query = query.filter(FlightRoute.arrival_airport_id.__eq__(to_airport))
    if start_day:
        start_day = datetime.strptime(start_day[2:] + ' 00:00:00', '%y-%m-%d %H:%M:%S')
        query = query.filter(Flight.takeoff_time.__ge__(start_day))
    return query.all()


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


def get_all_flight():
    return Flight.query.all()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def get_all_airport():
    return Airport.query.all()


def get_all_user_by_role(role_id=UserRoleEnum.EMPLOYEE):
    return User.query.filter(User.user_role == role_id)


def auth_user(username, password, user_role=UserRoleEnum.USER):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password),
                             User.user_role.__eq__(user_role)).first()


def check_username(username):
    return True if db.session.query(User.username).filter(User.username.__eq__(username)).first() else False


if __name__ == '__main__':
    with app.app_context():
        print(get_flight(from_airport=2, to_airport=1, start_day='2022-12-25'))