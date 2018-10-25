#!/bin/sh
DATABASE="host_checker"
USERNAME="postgres"
HOSTNAME="127.0.0.1"
export PGPASSWORD="mysecretpassword"

psql -h $HOSTNAME -U $USERNAME -v ON_ERROR_STOP=1 <<-EOSQL
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
  port INT,
  is_active boolean,
  UNIQUE(id),
  UNIQUE(host, port)

);
CREATE TABLE users_hosts(
  user_id int REFERENCES users (id) ON UPDATE CASCADE ON DELETE CASCADE,
  host_id int REFERENCES hosts (id) ON UPDATE CASCADE ON DELETE CASCADE,
  PRIMARY KEY (user_id, host_id)
)
CREATE OR REPLACE FUNCTION host_cleanup(int) RETURNS void as $$
DECLARE
total int;
BEGIN
  SELECT count(*) into total from users_hosts where host_id=$1;
  IF (total = 0) THEN
    DELETE FROM hosts WHERE id = $1;
  END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_last_host
  AFTER DELETE ON users_hosts REFERENCING OLD ROW AS old_row
  FOR EACH ROW
  EXECUTE PROCEDURE host_cleanup(old_row.host_id);
EOSQL
