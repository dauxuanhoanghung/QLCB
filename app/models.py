from sqlalchemy import Column, Integer, Boolean, Float, String, Text, ForeignKey, Enum, DateTime, Time
from sqlalchemy.orm import relationship, backref
from app import db, app
from datetime import datetime
from enum import Enum as UserEnum
from flask_login import UserMixin


class UserRoleEnum(UserEnum):
    USER = 1
    EMPLOYEE = 2
    ADMIN = 3


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class User(BaseModel, UserMixin):
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    name = Column(String(80), nullable=False)
    identity_number = Column(String(15))
    email = Column(String(80))
    phone_number = Column(String(15))
    avatar = Column(Text)
    is_active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)

    def __str__(self):
        return self.name


class Airport(BaseModel):
    name = Column(String(80), nullable=False)
    location = Column(String(100), nullable=False)
    picture = Column(String(200))

    def __str__(self):
        return '{0} - {1}'.format(self.name, self.location)


class FlightRoute(BaseModel):
    arrival_airport_id = Column(Integer, ForeignKey(Airport.id), nullable=False)
    departure_airport_id = Column(Integer, ForeignKey(Airport.id), nullable=False)
    departure_airport = relationship('Airport', backref='flight_route1', lazy=True,
                                     foreign_keys='FlightRoute.departure_airport_id')
    arrival_airport = relationship('Airport', backref='flight_route2', lazy=True,
                                   foreign_keys='FlightRoute.arrival_airport_id')

    def __str__(self):
        return self.departure_airport.location + ' - ' + self.arrival_airport.location


# class ArrivalAirportOfRoute(BaseModel):
#     arrival_airport_id = Column(Integer, ForeignKey(Airport.id), nullable=False)
#     flight_route_id = Column(Integer, ForeignKey(FlightRoute.id), nullable=False)
# class DepartureAirportOfRoute(BaseModel):
#     departure_airport_id = Column(Integer, ForeignKey(Airport.id), nullable=False)
#     flight_route_id = Column(Integer, ForeignKey(FlightRoute.id), nullable=False)


class Airplane(BaseModel):
    name = Column(String(15), nullable=False)
    number_of_seat = Column(Integer, nullable=False, default=80)
    seats = relationship('Seat', backref='airplane', lazy=True)

    def __str__(self):
        return self.name


class Flight(BaseModel):
    takeoff_time = Column(DateTime, nullable=False)
    landing_time = Column(DateTime, nullable=False)
    flying_time = Column(Time, default=landing_time-takeoff_time)
    base_price = Column(Float, default=0)
    airplane_id = Column(Integer, ForeignKey(Airplane.id), nullable=False)
    flight_route_id = Column(Integer, ForeignKey(FlightRoute.id), nullable=False)

    airplane = relationship(Airplane, backref='flights', lazy=True)
    flight_route = relationship(FlightRoute, backref='flights', lazy=True)
    transit_airports = relationship('TransitAirport', backref='flights', lazy=True)
    tickets = relationship('Ticket', backref='flight', lazy=True)

    def __str__(self):
        return str(self.flight_route) + ' vào ' + str(self.takeoff_time)


class TransitAirport(BaseModel):
    break_time = Column(DateTime, nullable=False)
    flight_id = Column(Integer, ForeignKey(Flight.id), nullable=False)
    airport_id = Column(Integer, ForeignKey(Airport.id), nullable=False)
    airport = relationship('Airport', backref='transit_airports', lazy=True)


class Seat(BaseModel):
    seat_number = Column(Integer, nullable=False)
    airplane_id = Column(Integer, ForeignKey(Airplane.id), nullable=False)


class TicketType(BaseModel):
    type = Column(String(50), nullable=False)

    tickets = relationship('Ticket', backref='ticket_type', lazy=True)

    def __str__(self):
        return self.type


class Ticket(BaseModel):
    ticket_price = Column(Float, nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    ticket_type_id = Column(Integer, ForeignKey(TicketType.id), nullable=False)
    flight_id = Column(Integer, ForeignKey(Flight.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)


class Regulation(BaseModel):
    name = Column(Text)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
