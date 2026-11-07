-- Creates the database hbtn_0d_usa and the table states in it
-- Creates the database hbtn_0d_usa if it does not already exist
CREATE DATABASE IF NOT EXISTS hbtn_0d_usa;
-- Creates states in hbtn_0d_usa if the table does not already exist
CREATE TABLE IF NOT EXISTS hbtn_0d_usa.states (id INT UNIQUE NOT NULL AUTO_INCREMENT PRIMARY KEY, name VARCHAR(256) NOT NULL);
