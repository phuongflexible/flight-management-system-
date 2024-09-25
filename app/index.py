from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from urllib.parse import quote
from app.admin import *
import os, hashlib
from datetime import datetime, time, timedelta
from app.models import UserRole, Customer, Ticket
from app import flightapp, login_manager
from sqlalchemy import and_, or_, func
from app.models import db


# Duong dan den trang chu
@flightapp.route("/")
def home():
    return render_template("home.html", current_user=current_user)


# Duong dan den trang dang nhap
@flightapp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password)).first()
        print(user)

        if user:
            login_user(user=user)
            if user.user_role == UserRole.ADMIN:
                return redirect("/report")
            else:
                return redirect("/book_tickets")
        else:
            flash('Tên người dùng hoặc mật khẩu không đúng!')
            return redirect(url_for('login'))

    if request.method == 'GET':
        if current_user.is_authenticated:
            if current_user.user_role == UserRole.ADMIN:
                return redirect(url_for('admin.index'))
            elif current_user.user_role == UserRole.STAFF:
                return redirect("/book_tickets")
            else:
                return redirect("/")
        else:
            return render_template("login.html", current_user=current_user)


# Duong dan den trang dat ve
@flightapp.route("/book_tickets", methods=['GET', 'POST'])
def book_tickets():
    airport_start = request.args.get('airport_start')
    airport_destination = request.args.get('airport_destination')
    airport_departure_date = request.args.get('airport_departure_date')

    twelve_hours_ago = datetime.now() - timedelta(hours=10)
    flights = Flight.query.filter(and_(Flight.departure_time >= twelve_hours_ago),
                                  or_(Flight.availableClassFirstSeat > 0, Flight.availableClassSecondSeat > 0)).all()

    formSearchFlight = FormSearchFlight()
    if formSearchFlight.validate_on_submit():
        start_id = formSearchFlight.start.data
        destination_id = formSearchFlight.destination.data
        departure_date = formSearchFlight.departure_date.data
        # print(start_id)
        # print(destination_id)
        # print(departure_date)

        flights = (Flight.query.join(Route, Flight.route_id == Route.id)
                   .filter(Route.departure_id == start_id, Route.destination_id == destination_id,
                           Flight.departure_time >= twelve_hours_ago,
                           or_(Flight.availableClassFirstSeat > 0, Flight.availableClassSecondSeat > 0)).all())

    return render_template("book_tickets.html", current_user=current_user, flights=flights,
                           formSearchFlight=formSearchFlight)


# Duong dan den trang mua ve
@flightapp.route("/buy_tickets", methods=['POST'])
def buy_tickets():
    if request.method == 'POST':
        referrerPage = request.referrer.split("/")[-1]
        employeeId = request.form['employee_id']
        flightId = request.form['flight_id']
        flightCode = request.form['flight_code']
        routeId = request.form['route_id']
        startName = request.form['start_name']
        destinationName = request.form['destination_name']
        departureTime = request.form['departure_time']
        arrivalTime = request.form['arrival_time']
        seatClass = request.form['seat_class']
        seatPrice = request.form['seat_price']

        return render_template("buy_tickets.html", flightId=flightId,
                               flightCode=flightCode, routeId=routeId, startName=startName,
                               destinationName=destinationName,
                               departureTime=departureTime, arrivalTime=arrivalTime, seatClass=seatClass,
                               seatPrice=seatPrice,
                               employeeId=employeeId, referrerPage=referrerPage)
    return redirect((url_for('book_tickets')))


# Duong dan den luu ve
@flightapp.route("/save_ticket", methods=['POST'])
def save_ticket():
    flightId = request.form['flightId']
    seatClass = request.form['seatClass']
    seatPrice = request.form['seatPrice']
    employeeId = request.form['employeeId']
    fullName = request.form['fullName']
    identityCard = request.form['identityCard']
    phoneNumber = request.form['phoneNumber']
    address = request.form['address']
    bankNumber = request.form['bankNumber']
    referrerPage = request.form['referrerPage']
    routeId = request.form['routeId']

    if not (employeeId):
        employeeId = None

    # -- save customer
    customer = Customer(fullname=fullName, identityCard=identityCard,
                        address=address, phoneNumber=phoneNumber, bankNumber=bankNumber)
    db.session.add(customer)
    db.session.commit()
    customerId = customer.id

    # -- save ticket
    ticket = Ticket(flight_id=flightId, customer_id=customerId, staff_id=employeeId, route_id=routeId,
                    seat_class=seatClass, seat_price=seatPrice)
    db.session.add(ticket)
    db.session.commit()

    # -- update seat of flight
    flight = Flight.query.get(flightId)
    if seatClass == "Hạng 1":
        flight.availableClassFirstSeat = flight.availableClassFirstSeat - 1
    else:
        flight.availableClassSecondSeat = flight.availableClassSecondSeat - 1
    db.session.commit()

    # --
    return render_template("tickets.html", flight=flight, ticket=ticket,
                           customer=customer, employeeId=employeeId, referrerPage=referrerPage)


# Duong dan den trang ban ve
@flightapp.route("/ticket_sales", methods=['GET', 'POST'])
@login_required
def ticket_sales():
    if request.method == 'GET':
        if not current_user.is_authenticated:
            return redirect(url_for('login'))

    employeeId = current_user.id
    airport_start = request.args.get('airport_start')
    airport_destination = request.args.get('airport_destination')
    airport_departure_date = request.args.get('airport_departure_date')

    twelve_hours_ago = datetime.now() - timedelta(hours=10)
    flights = Flight.query.filter(and_(Flight.departure_time >= twelve_hours_ago),
                                  or_(Flight.availableClassFirstSeat > 0, Flight.availableClassSecondSeat > 0)).all()

    formSearchFlight = FormSearchFlight()
    if formSearchFlight.validate_on_submit():
        start_id = formSearchFlight.start.data
        destination_id = formSearchFlight.destination.data
        departure_date = formSearchFlight.departure_date.data

        flights = (Flight.query.join(Route, Flight.route_id == Route.id)
                   .filter(Route.departure_id == start_id, Route.destination_id == destination_id,
                           Flight.departure_time >= twelve_hours_ago,
                           or_(Flight.availableClassFirstSeat > 0, Flight.availableClassSecondSeat > 0)).all())

    return render_template("ticket_sales.html", current_user=current_user,
                           flights=flights, formSearchFlight=formSearchFlight, employeeId=employeeId)


# Duong dan den trang thong ke bao cao
@flightapp.route("/report", methods=['GET', 'POST'])
@login_required
def report():
    now = datetime.now()
    if request.method == 'POST':
        month = request.form['month']
        year = request.form['year']
    else:
        month = now.strftime("%m")
        year = now.strftime("%Y")

    #Tạo bi danh cho bang Airport
    airport_alias_1 = db.aliased(Airport)
    airport_alias_2 = db.aliased(Airport)

    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    revenue_by_route = db.session.query(Flight.route_id, airport_alias_1.name, airport_alias_2.name,
                                        func.sum(Ticket.seat_price)). \
        join(Ticket, Flight.id == Ticket.flight_id). \
        join(Route, Flight.route_id == Route.id). \
        join(airport_alias_1, Route.departure_id == airport_alias_1.id). \
        join(airport_alias_2, Route.destination_id == airport_alias_2.id). \
        filter(db.extract('year', Flight.departure_time) == year, db.extract('month', Flight.departure_time) == month). \
        group_by(Flight.route_id).all()

    #In nội dung truy vấn
    print(revenue_by_route)

    flights_by_route = db.session.query(Flight.route_id, func.count(Flight.id)).\
        filter(db.extract('year', Flight.departure_time) == year,
               db.extract('month', Flight.departure_time) == month).\
        group_by(Flight.route_id).all()
    print("CCCCCCCCCCCCCCCCCCCCCC")
    print(flights_by_route)
    total_revenue = sum(t[-1] for t in revenue_by_route)
    print("DDDDDDDDDDDDDDDDDDDDDDDDD")
    print(total_revenue)
    #Tinh toan ty le doanh thu theo tuyen bay
    report_data = []
    for route_id, airport_start_name, airport_destination_name, revenue in revenue_by_route:
        flights = next((flights for route, flights in flights_by_route if route == route_id), 0)
        revenue_rate = (revenue / total_revenue) * 100 if total_revenue > 0 else 0
        report_data.append((route_id, airport_start_name, airport_destination_name, revenue, flights, revenue_rate))

    print(report_data)
    return render_template("report.html", report_data=report_data,
                           total_revenue=total_revenue, month=int(month), year=int(year), now=now)

#Dang xuat
@flightapp.route("/logout")
def logout():
    logout_user()
    return redirect('/')


# callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    flightapp.run(debug=True)
