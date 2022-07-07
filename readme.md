first, open command prompt/terminal , and go to the project directory
once in the project directory, run the following

first, install packages listed in requirements.txt by


set FLASK_APP=main.py
set FLASK_DEBUG=1
flask run

next, open mysql server, and run following, to create a database and tables within it

1. CREATE DATABASE loginwebsite;

2. USE loginwebsite;

3. CREATE TABLE IF NOT EXISTS user(
username varchar(50) NOT NULL,
password varchar(255) NOT NULL,
email varchar(100) NOT NULL
);
