-- create database and user -- and grant privileges
create database if not exists learnplus;
create user if not exists 'learnplus'@'localhost' identified by "Aa48904890plmn$";
grant all privileges on learnplus.* to 'learnplus'@'localhost';
