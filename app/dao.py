import calendar
from datetime import datetime
from app.models import *
from app import db, app
from flask_login import current_user
from sqlalchemy import func, or_, and_
import hashlib


def get_all_ticket_type():
    return TicketType.query.all()


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


def get_all_flight(page=1):
    page_size = app.config['page_size']
    start = (page - 1) * page_size
    end = start + page_size
    return Flight.query.filter(Flight.takeoff_time.__ge__(datetime.now())).slice(start, end).all()


def count_flights():
    return Flight.query.filter(Flight.takeoff_time.__ge__(datetime.now())).count()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def count_user_tickets():
    if current_user.is_authenticated:
        return len(current_user.tickets)
    return 0


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


def get_flight(from_airport=None, to_airport=None, start_day=None):
    query = Flight.query.join(FlightRoute, Flight.flight_route_id.__eq__(FlightRoute.id))
    if from_airport:
        query = query.filter(FlightRoute.departure_airport_id.__eq__(from_airport))
    if to_airport:
        query = query.filter(FlightRoute.arrival_airport_id.__eq__(to_airport))
    if start_day:
        start_day = datetime.strptime(start_day[2:] + ' 00:00:00', '%y-%m-%d %H:%M:%S')
        query = query.filter(Flight.takeoff_time.__ge__(start_day))
    return query.all()


def get_flight_by_id(id):
    return Flight.query.filter(Flight.id.__eq__(id)).first()


def save_ticket(ticket_price, flight_id, ticket_type_id):
    ticket = Ticket(ticket_price=ticket_price, flight_id=flight_id, ticket_type_id=ticket_type_id,
                    user_id=current_user.id)
    db.session.add(ticket)
    db.session.commit()


def get_tickets_by_user_id(user_id):
    return Ticket.query.filter(user_id.__eq__(Ticket.user_id)).all()


def count_flights_by_month(month, year):
    return Flight.query.filter(and_(Flight.takeoff_time.__ge__(datetime(
        year=year, month=month, day=1)),
        Flight.takeoff_time.__le__(datetime(year=year, month=month, day=calendar.monthrange(year, month)[1])))).count()


def stats_revenue(month, year):
    fl = db.session.query
    query = db.session.query(FlightRoute.id, FlightRoute, func.count(Flight.id), func.sum(Ticket.ticket_price)) \
        .join(Flight, and_(Flight.takeoff_time.__ge__(datetime(
        year=year, month=month, day=1)),
        Flight.takeoff_time.__le__(datetime(year=year, month=month, day=calendar.monthrange(year, month)[1])),
        Flight.flight_route_id.__eq__(FlightRoute.id)), isouter=True) \
        .join(Ticket, Ticket.flight_id.__eq__(Flight.id), isouter=True)
    return query.group_by(FlightRoute.id).all()


if __name__ == '__main__':
    with app.app_context():
        # print(count_flights_by_month(12, 2022))
        print(stats_revenue(12, 2022))
        # print(get_flight(from_airport=2, to_airport=1, start_day='2022-12-25'))
