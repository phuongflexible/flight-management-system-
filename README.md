# Flight management system
A website which supports to manage flights.
## Table of contents
* [General Information](#general-information)
* [Technology used](#technology-used)
* [Features](#features)
* [Setup](#setup)
* [Project status](#project-status)
## General Information
A website to provide necessary functions for booking tickets and managing flights of the airports. Users can book ticket online thanks to this web. Ticket staff can sell tickets at the counter and admin can manage informations related to flights.
## Technology used
- Python: programming language. Version: 3.12.1.
- Python Flask: a web framework which helps to build and develop a web application.
- MySQL: a database management system which is used to manage data.
## Features
### 1. Book tickets:
- This function helps customers to book tickets online. Custormers can use the filter to find information about the flights they would like to book. They only allowed to book tickets for flights which is going to taking off after twelve hours since the booking time.
### 2. Sell tickets:
- This function helps ticket staff sell tickets to customers at the counter, the staff can look up information which is classified by flights, departure time.
### 3. Make a flight schedule:
- This function allows admin to make a schedule for a flight. Admin has to arrange schedules based on these rules: There are ten airports, the minimum time of flight duration is 30 minutes, there are two transit airports in maximum and transit time is from 20 to 30 minutes.
### 4. Statistic:
- Admin can see statistic in the form of table and chart: statistic about revenue of each month which is classified by routes.
### 5. Change the rules:
Admin is allowed to:
- Chage the number of airports, the minimum time of flight duration, the number of transit airports in maximum, transit time in minimum and maximum at transit airport.
- Manage routes, flights, users.
## Setup
### To run this project:
- Make sure the equipments has downloaded python.
- Use IDE like Pycharm or Visual Studio Code to run the project.
- Create virtual environment.
- Install everything according to file requirements.txt .
- Create a database in MySQL and declare the database's name and password of MySQL in file \_\_init_\_\.py . Fill in:
  "mysql+pymysql://root:%s@localhost/_database's name_?charset=utf8mb4" % quote ("_password_")
- Run file models.py to download data into database in MySQL.
- Run file index.py to run the project.
## Project status
This project is complete.

