import datetime
from flask import Flask
from app import db, flightapp
from sqlalchemy import Column, Integer, String, Boolean, Float, Enum, DateTime, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
import hashlib
from enum import Enum as UserEnum
from flask_login import UserMixin


class Airport(db.Model):   #San bay
    __tablename__ = 'airport'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(10), unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    address = Column(String(50), nullable=False)

    #transits = relationship("Transit", backref="Airport", lazy=True)  # 1 san bay la cua nhieu san bay trung gian
    #routes = relationship("Route", primaryjoin="and_(Airport.id==Route.departure_id, Airport.id==Route.destination_id)", backref="airport", lazy=True)
    #1 san bay la san bay di/den cua nhieu tuyen bay


class Route(db.Model):   #tuyen bay
    __tablename__ = 'route'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    departure_id = Column(Integer, ForeignKey(Airport.id), nullable=False)
    destination_id = Column(Integer, ForeignKey(Airport.id), nullable=False)

    departure = relationship("Airport", foreign_keys=[departure_id])
    destination = relationship("Airport", foreign_keys=[destination_id])

class Flight(db.Model):    #chuyen bay
    __tablename__ = "flight"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    numberOfClassFirstSeat = Column(Integer, nullable=False)
    numberOfClassSecondSeat = Column(Integer, nullable=False)
    availableClassFirstSeat = Column(Integer, nullable=False)
    availableClassSecondSeat = Column(Integer, nullable=False)
    departure_time = Column(DateTime, nullable=False)
    destination_time = Column(DateTime, nullable=False)
    route_id = Column(Integer, ForeignKey(Route.id), nullable=False)
    unitPriceOfClassFirstSeat = Column(Float, nullable=False)
    unitPriceOfClassSecondSeat = Column(Float, nullable=False)

    route = relationship("Route", foreign_keys=[route_id], backref="route")
    transits = relationship("Flight_Transit", backref="flight")


class Transit(db.Model):  #san bay trung gian
    __tablename__ = "transit"
    id = Column(Integer, primary_key=True, autoincrement=True)
    duration = Column(String(20), nullable=False)
    airport_id = Column(Integer, ForeignKey("airport.id"), nullable=False)

    airport = relationship("Airport", foreign_keys=[airport_id])
    #flights = relationship("Flight_Transit", backref="transit")


class Flight_Transit(db.Model):   #Chuyen bay _ san bay trung gian
    __tablename__ = "flight_transit"
    flight_id = Column(Integer, ForeignKey(Flight.id), primary_key=True)
    transit_id = Column(Integer, ForeignKey(Transit.id), primary_key=True)


class Customer(db.Model):   #khach hang
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String(50), nullable=False)
    identityCard = Column(String(20), unique=True, nullable=False)
    phoneNumber = Column(String(10), unique=True, nullable=False)
    address = Column(String(50), nullable=False)
    bankNumber = Column(String(20), nullable=False)

    tickets = relationship('Ticket', backref='customer', lazy=True)  # 1 khach hang co the mua nhieu ve


class Staff(db.Model):   #nhan vien
    __tablename__ = 'staff'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String(50), nullable=False)

    tickets = relationship('Ticket', backref='staff', lazy=True)  # 1 nhan vien ban nhieu ve


class Ticket(db.Model):   #ve
    __tablename__ = 'ticket'
    id = Column(Integer, primary_key=True, autoincrement=True)
    staff_id = Column(Integer, ForeignKey(Staff.id), nullable=True)
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)
    flight_id = Column(Integer, ForeignKey(Flight.id), nullable=False)
    route_id = Column(Integer, ForeignKey(Route.id), nullable=False)
    seat_class = Column(String(50), nullable=False)
    seat_price = Column(Float, nullable=False)


"""*==USER*==="""
class UserRole(UserEnum):
    ADMIN = 1
    STAFF = 2


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.STAFF)


if __name__ == '__main__':
    with flightapp.app_context():
        db.drop_all()
        db.create_all()


        airports = [
            Airport(code='HAN', name='Hà Nội', address='Địa chỉ 1'),
            Airport(code='HPH', name='Hải Phòng', address='Địa chỉ 2'),
            Airport(code='THD', name='Thanh Hóa', address='Địa chỉ 3'),
            Airport(code='VDO', name='Vân Đồn', address='Địa chỉ 4'),
            Airport(code='DIN', name='Điện Biên', address='Địa chỉ 5'),
            Airport(code='DAD', name='Đà Nẵng', address='Địa chỉ 6'),
            Airport(code='HUI', name='Huế', address='Địa chỉ 7'),
            Airport(code='TBB', name='Tuy Hòa', address='Địa chỉ 8'),
            Airport(code='SGN', name='Hồ Chí Minh', address='Địa chỉ 9'),
            Airport(code='PQC', name='Phú Quốc', address='Địa chỉ 10'),

        ]
        db.session.add_all(airports)
        db.session.commit()


        customers = [
            Customer(fullname='Nguyễn Văn A', identityCard='000000000000', phoneNumber="0000000000", address='Địa chỉ 001', bankNumber='BAKN0001'),
            Customer(fullname='Nguyễn Thị B', identityCard='111111111111', phoneNumber="1111111111", address='Địa chỉ 002', bankNumber='BAKN0002'),
            Customer(fullname='Trần Thị C', identityCard='222222222222', phoneNumber="2222222222", address='Địa chỉ 003', bankNumber='BAKN0003'),
            Customer(fullname='Lê Văn D', identityCard='333333333333', phoneNumber="3333333333", address='Địa chỉ 004', bankNumber='BAKN0004'),
            Customer(fullname='Lê Thị E', identityCard='444444444444', phoneNumber="4444444444", address='Địa chỉ 005', bankNumber='BAKN0005'),
            Customer(fullname='Đinh Văn F', identityCard='555555555555', phoneNumber="5555555555", address='Địa chỉ 006', bankNumber='BAKN0006'),
            Customer(fullname='Trần Văn G', identityCard='666666666666', phoneNumber="6666666666", address='Địa chỉ 007', bankNumber='BAKN0007'),
            Customer(fullname='Lý Thị H', identityCard='777777777777', phoneNumber="7777777777", address='Địa chỉ 008', bankNumber='BAKN0008'),
            Customer(fullname='Nguyễn Thị I', identityCard='888888888888', phoneNumber="8888888888", address='Địa chỉ 009', bankNumber='BAKN0009'),
            Customer(fullname='Đoàn Văn J', identityCard='999999999999', phoneNumber="0101010101", address='Địa chỉ 010', bankNumber='BAKN0010'),
        ]
        db.session.add_all(customers)
        db.session.commit()

        staff = [
            Staff(fullname="Nguyễn Đức Tuấn"),
            Staff(fullname='Lê Thị Kim Hoa'),
        ]
        db.session.add_all(staff)
        db.session.commit()


        routes = [
            Route(name='TP HCM (SGN) - Hà Nội (HAN)', departure_id=9, destination_id=1),
            Route(name='Phú Quốc (PQC) - TP HCM (SGN)', departure_id=10, destination_id=9),
            Route(name='Đà Nẵng (DAD) -  TP HCM (SGN)', departure_id=6, destination_id=9),
            Route(name='Hải Phòng (HPH) - Đà Nẵng (DAD)', departure_id=2, destination_id=6),
            Route(name='Hà Nội (HAN) - TP HCM (SGN)', departure_id=1, destination_id=9),
            Route(name='Hải Phòng (HPH) - Phú Quốc (PQC)', departure_id=2, destination_id=10),
            Route(name='Đà Nẵng (DAD) - Phú Quốc (PQC)', departure_id=2, destination_id=10),
            Route(name='Phú Quốc (PQC) - Hà Nội (HAN)', departure_id=10, destination_id=1),
            Route(name='Huế (HUI) - TPHCM (SGN)', departure_id=7, destination_id=10),
            Route(name='Hà Nôi (HAN) - Đà Nẵng (DAD)', departure_id=1, destination_id=6),


        ]
        db.session.add_all(routes)
        db.session.commit()


        flights = [
            Flight(name='FLY001', route_id='1', departure_time='2024-10-20 01:00:00',
                   destination_time='2024-10-20 02:30:00', numberOfClassFirstSeat='10', numberOfClassSecondSeat='100',
                   availableClassFirstSeat='0', availableClassSecondSeat='90', unitPriceOfClassFirstSeat='1000000',
                   unitPriceOfClassSecondSeat='100000'),
            Flight(name='FLY002', route_id='2', departure_time='2024-10-21 02:00:00',
                   destination_time='2024-10-21 03:30:00', numberOfClassFirstSeat='20', numberOfClassSecondSeat='200',
                   availableClassFirstSeat='20', availableClassSecondSeat='200', unitPriceOfClassFirstSeat='2000000',
                   unitPriceOfClassSecondSeat='200000'),
            Flight(name='FLY003', route_id='3', departure_time='2024-10-22 03:00:00',
                   destination_time='2024-10-22 04:30:00', numberOfClassFirstSeat='30', numberOfClassSecondSeat='300',
                   availableClassFirstSeat='30', availableClassSecondSeat='300', unitPriceOfClassFirstSeat='3000000',
                   unitPriceOfClassSecondSeat='300000'),
            Flight(name='FLY004', route_id='4', departure_time='2024-10-23 04:00:00',
                   destination_time='2024-10-23 05:30:00', numberOfClassFirstSeat='40', numberOfClassSecondSeat='400',
                   availableClassFirstSeat='40', availableClassSecondSeat='400', unitPriceOfClassFirstSeat='4000000',
                   unitPriceOfClassSecondSeat='400000'),
            Flight(name='FLY005', route_id='5', departure_time='2024-10-24 05:00:00',
                   destination_time='2024-10-24 06:30:00', numberOfClassFirstSeat='50', numberOfClassSecondSeat='500',
                   availableClassFirstSeat='50', availableClassSecondSeat='500', unitPriceOfClassFirstSeat='5000000',
                   unitPriceOfClassSecondSeat='500000'),
            Flight(name='FLY006', route_id='6', departure_time='2024-10-25 06:00:00',
                   destination_time='2024-10-25 07:30:00', numberOfClassFirstSeat='60', numberOfClassSecondSeat='600',
                   availableClassFirstSeat='60', availableClassSecondSeat='600', unitPriceOfClassFirstSeat='6000000',
                   unitPriceOfClassSecondSeat='600000'),
            Flight(name='FLY007', route_id='7', departure_time='2024-10-26 07:00:00',
                   destination_time='2024-10-26 08:30:00', numberOfClassFirstSeat='70', numberOfClassSecondSeat='700',
                   availableClassFirstSeat='70', availableClassSecondSeat='700', unitPriceOfClassFirstSeat='7000000',
                   unitPriceOfClassSecondSeat='700000'),
            Flight(name='FLY008', route_id='8', departure_time='2024-10-27 08:00:00',
                   destination_time='2024-10-27 09:30:00', numberOfClassFirstSeat='80', numberOfClassSecondSeat='800',
                   availableClassFirstSeat='80', availableClassSecondSeat='800', unitPriceOfClassFirstSeat='8000000',
                   unitPriceOfClassSecondSeat='800000'),
            Flight(name='FLY009', route_id='9', departure_time='2024-10-28 09:00:00',
                   destination_time='2024-10-28 10:30:00', numberOfClassFirstSeat='90', numberOfClassSecondSeat='900',
                   availableClassFirstSeat='90', availableClassSecondSeat='900', unitPriceOfClassFirstSeat='9000000',
                   unitPriceOfClassSecondSeat='900000'),
            Flight(name='FLY010', route_id='10', departure_time='2024-10-29 10:00:00',
                   destination_time='2024-10-29 11:30:00', numberOfClassFirstSeat='100', numberOfClassSecondSeat='1000',
                   availableClassFirstSeat='100', availableClassSecondSeat='1000', unitPriceOfClassFirstSeat='10000000',
                   unitPriceOfClassSecondSeat='1000000'),

            Flight(name='FLY011', route_id='1', departure_time='2024-10-30 01:00:00',
                   destination_time='2024-10-30 02:30:00', numberOfClassFirstSeat='10', numberOfClassSecondSeat='100',
                   availableClassFirstSeat='0', availableClassSecondSeat='90', unitPriceOfClassFirstSeat='1000000',
                   unitPriceOfClassSecondSeat='100000'),
            Flight(name='FLY012', route_id='2', departure_time='2024-10-31 02:00:00',
                   destination_time='2024-10-31 03:30:00', numberOfClassFirstSeat='20', numberOfClassSecondSeat='200',
                   availableClassFirstSeat='20', availableClassSecondSeat='200', unitPriceOfClassFirstSeat='2000000',
                   unitPriceOfClassSecondSeat='200000'),
            Flight(name='FLY013', route_id='3', departure_time='2024-11-01 03:00:00',
                   destination_time='2024-11-01 04:30:00', numberOfClassFirstSeat='30', numberOfClassSecondSeat='300',
                   availableClassFirstSeat='30', availableClassSecondSeat='300', unitPriceOfClassFirstSeat='3000000',
                   unitPriceOfClassSecondSeat='300000'),
            Flight(name='FLY014', route_id='4', departure_time='2024-11-02 04:00:00',
                   destination_time='2024-11-02 05:30:00', numberOfClassFirstSeat='40', numberOfClassSecondSeat='400',
                   availableClassFirstSeat='40', availableClassSecondSeat='400', unitPriceOfClassFirstSeat='4000000',
                   unitPriceOfClassSecondSeat='400000'),
            Flight(name='FLY015', route_id='5', departure_time='2024-11-03 05:00:00',
                   destination_time='2024-11-03 06:30:00', numberOfClassFirstSeat='50', numberOfClassSecondSeat='500',
                   availableClassFirstSeat='50', availableClassSecondSeat='500', unitPriceOfClassFirstSeat='5000000',
                   unitPriceOfClassSecondSeat='500000'),
            Flight(name='FLY016', route_id='6', departure_time='2024-11-04 06:00:00',
                   destination_time='2024-11-04 07:30:00', numberOfClassFirstSeat='60', numberOfClassSecondSeat='600',
                   availableClassFirstSeat='60', availableClassSecondSeat='600', unitPriceOfClassFirstSeat='6000000',
                   unitPriceOfClassSecondSeat='600000'),
            Flight(name='FLY017', route_id='7', departure_time='2024-11-05 07:00:00',
                   destination_time='2024-11-05 08:30:00', numberOfClassFirstSeat='70', numberOfClassSecondSeat='700',
                   availableClassFirstSeat='70', availableClassSecondSeat='700', unitPriceOfClassFirstSeat='7000000',
                   unitPriceOfClassSecondSeat='700000'),
            Flight(name='FLY018', route_id='8', departure_time='2024-11-05 08:00:00',
                   destination_time='2024-11-05 09:30:00', numberOfClassFirstSeat='80', numberOfClassSecondSeat='800',
                   availableClassFirstSeat='80', availableClassSecondSeat='800', unitPriceOfClassFirstSeat='8000000',
                   unitPriceOfClassSecondSeat='800000'),
            Flight(name='FLY019', route_id='9', departure_time='2024-11-06 09:00:00',
                   destination_time='2024-11-06 10:30:00', numberOfClassFirstSeat='90', numberOfClassSecondSeat='900',
                   availableClassFirstSeat='90', availableClassSecondSeat='900', unitPriceOfClassFirstSeat='9000000',
                   unitPriceOfClassSecondSeat='900000'),
            Flight(name='FLY020', route_id='10', departure_time='2024-11-07 10:00:00',
                   destination_time='2024-11-07 11:30:00', numberOfClassFirstSeat='100', numberOfClassSecondSeat='1000',
                   availableClassFirstSeat='90', availableClassSecondSeat='900', unitPriceOfClassFirstSeat='10000000',
                   unitPriceOfClassSecondSeat='1000000')
        ]
        db.session.add_all(flights)
        db.session.commit()

        transits = [
            Transit(airport_id=4, duration="00:20:00"),
            Transit(airport_id=9, duration="00:30:00"),
            Transit(airport_id=6, duration="00:25:00"),
            Transit(airport_id=5, duration="00:20:00"),
           
        ]
        db.session.add_all(transits)
        db.session.commit()


        flight_transit = [
            Flight_Transit(flight_id=1, transit_id=2),
            Flight_Transit(flight_id=3, transit_id=4),
        ]
        db.session.add_all(flight_transit)
        db.session.commit()


        tickets = [
            Ticket(staff_id=2, customer_id=4, flight_id=1, route_id=1, seat_class="Hạng 1", seat_price="1000000"),
            Ticket(staff_id=2, customer_id=8, flight_id=3, route_id=4, seat_class="Hạng 2", seat_price="1000000"),
            Ticket(staff_id=2, customer_id=2, flight_id=2, route_id=2, seat_class="Hạng 1", seat_price="1000000"),
            Ticket(staff_id=2, customer_id=5, flight_id=1, route_id=1, seat_class="Hạng 2", seat_price="1000000"),
            Ticket(staff_id=2, customer_id=5, flight_id=10, route_id=5, seat_class="Hạng 2", seat_price="1000000"),
            Ticket(staff_id=2, customer_id=7, flight_id=11, route_id=2, seat_class="Hạng 2", seat_price="1000000"),
            Ticket(staff_id=2, customer_id=10, flight_id=11, route_id=4, seat_class="Hạng 2", seat_price="1000000"),
            Ticket(staff_id=2, customer_id=1, flight_id=20, route_id=10, seat_class="Hạng 2", seat_price="1000000"),
            Ticket(staff_id=2, customer_id=3, flight_id=15, route_id=1, seat_class="Hạng 2", seat_price="1000000"),
        ]
        db.session.add_all(tickets)
        db.session.commit()

        users = [
            User(name='Tuấn', username='ndtuan', password='12345', active=True, user_role=UserRole.ADMIN),
            User(name='Hoa', username='ltkhoa', password='12345', active=True, user_role=UserRole.STAFF),
        ]
        db.session.add_all(users)
        db.session.commit()






















