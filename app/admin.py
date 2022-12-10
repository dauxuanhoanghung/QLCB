from app import app, db, dao
from flask import request, redirect
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import logout_user, current_user
from app.models import UserRoleEnum, Flight, FlightRoute, Airport, TransitAirport


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN


class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class AirportModelView(ModelView):
    column_filters = ['name', 'location']
    column_display_pk = False
    column_labels = {
        'name': 'Mã Sân bay',
        'location': 'Địa điểm',
    }
    column_exclude_list = ('picture', )
    form_excluded_columns = ('flight_route1', 'flight_route2')

    def is_editable(self, name):
        return current_user.is_authenticated


class FlightRouteModelView(ModelView):
    column_display_pk = False
    can_create = True
    can_edit = True
    can_delete = True
    column_labels = {
        'departure_airport': 'Sân bay khởi hành',
        'arrival_airport': 'Sân bay đến',
    }
    column_sortable_list = ('departure_airport_id', 'arrival_airport_id')
    page_size = 12
    form_columns = ('departure_airport', 'arrival_airport',)


class FlightModelView(ModelView):
    column_labels = {
        'airplane': 'Máy bay',
        'flight_route': 'Tuyến bay',
        'takeoff_time': 'Thời gian khởi hành',
        'landing_time': 'Thời gian hạ cánh',
        'base_price': 'Giá vé cơ bản'
    }
    column_exclude_list = ('flying_time',)
    form_excluded_columns = ('transit_airports', 'tickets',)


class StatsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')


class MyAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')


class LogoutView(AuthenticatedView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


admin = Admin(app=app, name='Quản lý chuyến bay', template_mode='bootstrap4', index_view=MyAdminView())
admin.add_view(AirportModelView(Airport, db.session, name='Sân bay'))
admin.add_view(FlightModelView(Flight, db.session, name='Chuyến bay'))
admin.add_view(FlightRouteModelView(FlightRoute, db.session, name='Tuyến bay'))
admin.add_view(ModelView(TransitAirport, db.session, name='SB TG'))
admin.add_view(StatsView(name='Thống kê - báo cáo'))
admin.add_view(LogoutView(name='Đăng xuất'))
