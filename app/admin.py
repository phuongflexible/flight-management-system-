from flask_admin import Admin
from flask import Flask, redirect, url_for, request
from app import db, flightapp
from app.models import Airport, Route, Flight, Transit, Flight_Transit, User, UserRole
from flask_admin.contrib.sqla import ModelView
from flask_wtf import FlaskForm
from wtforms import DateField, FloatField, SelectField, StringField, IntegerField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_admin import BaseView, expose, AdminIndexView
from flask_login import logout_user, current_user


"""*===AUTHENTICATE===*"""
class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


"""*===FLIGHT===*"""
class FlightForm(FlaskForm):
    name = StringField('Mã chuyến bay', validators=[DataRequired()])
    numberOfClassFirstSeat = IntegerField('Số lượng ghế hạng 1', validators=[DataRequired()])
    numberOfClassSecondSeat = IntegerField('Số lượng ghế hạng 2', validators=[DataRequired()])
    departure_time = DateField('Ngày giờ khởi hành', format='%Y-%m-%d', validators=[DataRequired()])
    destination_time = DateField('Ngày giờ đến', format='%Y-%m-%d', validators=[DataRequired()])
    availableClassFirstSeat = IntegerField('Số lượng ghế hạng 1 còn trống', validators=[DataRequired()])
    availableClassSecondSeat = IntegerField('Số lượng ghế hạng 2 còn trống', validators=[DataRequired()])
    route = QuerySelectField('Tên tuyến bay', query_factory=lambda: Route.query.all(), get_label='name', validators=[DataRequired()])
    unitPriceOfClassFirstSeat = FloatField('Đơn giá ghế hạng 1', validators=[DataRequired()])
    unitPriceOfClassSecondSeat = FloatField('Đơn giá ghế hạng 2', validators=[DataRequired()])


class FlightView(AuthenticatedView):
    can_edit = True
    can_create = True
    can_delete = True
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['name']
    column_filters = ['name']
    column_list = ['id', 'name', 'numberOfClassFirstSeat', 'numberOfClassSecondSeat', 'departure_time', 'destination_time', 'availableClassFirstSeat',
                   'availableClassSecondSeat', 'route.name', 'unitPriceOfClassFirstSeat', 'unitPriceOfClassSecondSeat']
    column_labels = {
        'id': 'Mã chuyến bay',
        'name': 'Tên chuyến bay',
        'numberOfClassFirstSeat': 'Số lượng ghế hạng 1',
        'numberOfClassSecondSeat': 'Số lượng ghế hạng 2',
        'departure_time': 'Ngày giờ khởi hành',
        'destination_time': 'Ngày giờ đến',
        'availableClassFirstSeat': 'Số ghế hạng 1 còn trống',
        'availableClassSecondSeat': 'Số ghế hạng 2 còn trống',
        'route.name': 'Tên tuyến bay',
        'unitPriceOfClassFirstSeat': 'Đơn giá ghế hạng 1',
        'unitPriceOfClassSecondSeat': 'Đơn giá ghế hạng 2',
    }
    page_size = 50

    form = FlightForm

class FormSearchFlight(FlaskForm):
    with flightapp.app_context():
        start = SelectField('Start', choices=[(Airport.id, Airport.name) for Airport in Airport.query.all()],
                             validators=[DataRequired()])
        destination = SelectField('Destination', choices=[(Airport.id, Airport.name) for Airport in Airport.query.all()],
                             validators=[DataRequired()])
        departure_date = DateField('Departure date', format='%Y-%m-%d', validators=[DataRequired()])


"""*===TRANSIT===*"""
class TransitForm(FlaskForm):
    duration = StringField('Thời gian dừng', validators=[DataRequired()])
    airport = QuerySelectField('Tên sân bay', query_factory=lambda: Airport.query.all(), get_label='name', validators=[DataRequired()])

class TransitView(AuthenticatedView):
    can_edit = True
    can_create = True
    can_delete = True
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['airport.name']
    column_filters = ['airport.name']
    column_list = ['id', 'duration', 'airport.id', 'airport.name']
    column_labels = {
        'id': 'Mã sân bay trung gian',
        'duration': 'Thời gian dừng',
        'airport.id': 'Mã sân bay',
        'airport.name': 'Tên sân bay',
    }
    page_size = 50

    form = TransitForm


"""*===ROUTE===*"""
class RouteForm(FlaskForm):
    name = StringField('Tên tuyến bay', validators=[DataRequired()])
    departure = QuerySelectField('Sân bay xuất phát', query_factory=lambda: Airport.query.all(), get_label='name', validators=[DataRequired()])
    destination = QuerySelectField('Sân bay đích', query_factory=lambda: Airport.query.all(), get_label='name', validators=[DataRequired()])


class RouteView(AuthenticatedView):
    can_edit = True
    can_create = True
    can_delete = True
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['name', 'departure_id', 'destination_id']
    column_filters = ['name', 'departure_id', 'destination_id']
    column_list = ['id', 'name', 'departure.name', 'destination.name']
    column_labels = {
        'id': 'Mã tuyến bay',
        'name': 'Tên tuyến bay',
        'departure.name': 'Sân bay khởi hành',
        'destination.name': 'Sân bay đích đến'
    }
    #form_columns = ['name', 'departure_id', 'destination_id']
    page_size = 50

    form = RouteForm


"""*===AIRPORT===*"""
class AirportView(AuthenticatedView):
    can_edit = True
    can_create = True
    can_delete = True
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['name']
    column_filters = ['name']
    column_list = ['id', 'code', 'name', 'address']
    form_columns = ['code', 'name', 'address']
    column_labels = {
        'code': 'Mã sân bay',
        'name': 'Tên sân bay',
        'address': 'Địa chỉ'
    }
    page_size = 50


"""*===USER===*"""
class UserView(AuthenticatedView):
    can_edit = True
    can_create = True
    can_delete = True
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['name']
    column_filters = ['name']
    column_list = ['id', 'name', 'username', 'password', 'active', 'user_role']
    form_columns = ['name', 'username', 'password', 'user_role']
    column_labels = {
        'name': 'Tên',
        'username': 'Tên người dùng',
        'password': 'Mật khẩu',
        'active': 'Trạng thái',
        'user_role': 'Vai trò'
    }


"""*===LOGOUT===*"""
class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/')

    def is_accessible(self):
        return current_user.is_authenticated


"""*===ADMIN===*"""
class AdminView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    #redirect den trang login neu nguoi dung khong dang nhap
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))




admin = Admin(app=flightapp, name='HỆ THỐNG QUẢN LÝ CHUYẾN BAY', template_mode='bootstrap4')
index_view = AdminView(name="Trang chủ")
admin.add_view(AirportView(Airport, db.session, name="Sân bay"))
admin.add_view(TransitView(Transit, db.session, name="Sân bay trung gian"))
admin.add_view(RouteView(Route, db.session, name="Tuyến bay"))
admin.add_view(FlightView(Flight, db.session, name="Chuyến bay"))
admin.add_view(UserView(User, db.session, name="Nguời dùng"))
admin.add_view(LogoutView(name='Đăng xuất'))
