from app.models import *
from app import app, db, dao
from datetime import datetime
import hashlib

if __name__ == '__main__':
    with app.app_context():

        # apt1 = Airport(name='HAN', location='Hà Nội',
        #                picture='Ha_Noi.jpg')
        # apt2 = Airport(name='SGN', location='TP Hồ Chí Minh',
        #                picture='Ho_Chi_Minh_City.jpg')
        # apt3 = Airport(name='DAD', location='Đà Nẵng',
        #                picture='Da_Nang.jpg')
        # apt4 = Airport(name='VII', location='Nghệ An',
        #                picture='Vinh.jpg')
        # apt5 = Airport(name='HUI', location='Thừa Thiên - Huế',
        #                picture='Hue.jpg')
        # apt6 = Airport(name='CXR', location='Khánh Hòa',
        #                picture='Nha_Trang.jpg')
        # apt7 = Airport(name="DLI", location='Lâm Đồng',
        #                picture='Da_Lat.jpg')
        # db.session.add(apt1)
        # db.session.add(apt2)
        # db.session.add(apt3)
        # db.session.add(apt4)
        # db.session.add(apt5)
        # db.session.add(apt6)
        # db.session.add(apt7)
        #
        # apl1 = Airplane(name='Airbus A330', number_of_seat=85)
        # apl2 = Airplane(name='Airbus A350', number_of_seat=90)
        # apl3 = Airplane(name='Airbus A321')
        # apl4 = Airplane(name='Boeing 787')
        # apl5 = Airplane(name='ATR 72')
        # db.session.add(apl1)
        # db.session.add(apl2)
        # db.session.add(apl3)
        # db.session.add(apl4)
        # db.session.add(apl5)
        #
        # fl_route1 = FlightRoute(departure_airport_id=1, arrival_airport_id=2)
        # fl_route2 = FlightRoute(departure_airport_id=2, arrival_airport_id=1)
        # fl_route3 = FlightRoute(departure_airport_id=1, arrival_airport_id=3)
        # fl_route4 = FlightRoute(departure_airport_id=3, arrival_airport_id=1)
        # fl_route5 = FlightRoute(departure_airport_id=1, arrival_airport_id=4)
        # fl_route6 = FlightRoute(departure_airport_id=4, arrival_airport_id=1)
        # fl_route7 = FlightRoute(departure_airport_id=2, arrival_airport_id=3)
        # fl_route8 = FlightRoute(departure_airport_id=3, arrival_airport_id=2)
        # db.session.add(fl_route1)
        # db.session.add(fl_route2)
        # db.session.add(fl_route3)
        # db.session.add(fl_route4)
        # db.session.add(fl_route5)
        # db.session.add(fl_route6)
        # db.session.add(fl_route7)
        # db.session.add(fl_route8)
        flight1 = Flight(takeoff_time=datetime(year=2022, month=12, day=17, hour=16),
                         flying_time='10:00:00',
                         base_price=1750000,
                         airplane_id=1,
                         flight_route_id=4)
        flight2 = Flight(takeoff_time=datetime(year=2022, month=12, day=26, hour=6),
                         flying_time='10:00:00',
                         base_price=2650000,
                         airplane_id=2,
                         flight_route_id=7)
        flight3 = Flight(takeoff_time=datetime(year=2023, month=1, day=2, hour=3),
                         flying_time='10:00:00',
                         base_price=860000,
                         airplane_id=3,
                         flight_route_id=3)
        db.session.add(flight1)
        db.session.add(flight2)
        db.session.add(flight3)
        u = User(name='Administrator', username='admin',
                 password=str(hashlib.md5('123456'.strip().encode('utf-8')).hexdigest()),
                 user_role=UserRoleEnum.ADMIN)
        # e = User(name='NV1', username='emp',
        #          password=str(hashlib.md5('123456'.strip().encode('utf-8')).hexdigest()),
        #          user_role=UserRoleEnum.EMPLOYEE)
        db.session.add(u)
        # tk_type1 = TicketType(type="Hạng 1")
        # tk_type2 = TicketType(type="Hạng 2")
        # db.session.add(tk_type1)
        # db.session.add(tk_type2)
        # r = Regulation(min_flying_time='00:30:00', max_transit_airport=2, min_break_time='00:20:00',
        #                max_break_time='00:30:00', number_ticket_type=2, selling_time='4:00:00',
        #                booking_time='12:00:00')
        # db.session.add(r)
        db.session.commit()
