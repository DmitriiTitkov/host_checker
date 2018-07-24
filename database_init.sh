#!/bin/sh
DATABASE="host_checker"
USERNAME="postgres"
HOsTNAME="127.0.0.1"
export PGPASSWORD="mysecretpassword"

psql -h $HOSTNAME -U $USERNAME -v ON_ERROR_STOP=1 <<-EOSQL
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE DATABASE $DATABASE;
\c $DATABASE
CREATE TABLE users(
   id serial,
   login varchar(30) PRIMARY KEY,
   password varchar(120),
   UNIQUE(id)
   
);
CREATE TABLE hosts(
  id serial,
  host varchar(50),
  protocol char(3),
  port INT,
  status varchar(20),
  UNIQUE(id)

);
CREATE TABLE users_hosts(
  user_id int REFERENCES users (id) ON UPDATE CASCADE ON DELETE CASCADE,
  host_id int REFERENCES hosts (id) ON UPDATE CASCADE ON DELETE CASCADE,
  PRIMARY KEY (user_id, host_id)
)
EOSQL
