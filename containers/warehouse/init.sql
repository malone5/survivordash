CREATE USER survUser;

CREATE DATABASE metabase;
GRANT ALL PRIVILEGES ON DATABASE metabase TO survUser;

CREATE SCHEMA lake;
GRANT ALL PRIVILEGES ON SCHEMA lake TO survUser;

CREATE SCHEMA staging;
GRANT ALL PRIVILEGES ON SCHEMA staging TO survUser;