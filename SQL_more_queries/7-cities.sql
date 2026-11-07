-- Creates the database hbtn_0d_usa and the table cities in it
-- Creates the database hbtn_0d_usa if it does not already exist
CREATE DATABASE IF NOT EXISTS hbtn_0d_usa;
-- Creates cities in hbtn_0d_usa with state_id referencing states if the table does not already exist
CREATE TABLE IF NOT EXISTS hbtn_0d_usa.cities (id INT UNIQUE NOT NULL AUTO_INCREMENT PRIMARY KEY, state_id INT NOT NULL, name VARCHAR(256) NOT NULL, FOREIGN KEY (state_id) REFERENCES hbtn_0d_usa.states (id));
