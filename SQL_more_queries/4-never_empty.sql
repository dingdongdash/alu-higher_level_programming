-- Creates a table called id_not_null in the current database
-- Creates id_not_null with an id column that defaults to 1 if the table does not already exist
CREATE TABLE IF NOT EXISTS id_not_null (id INT DEFAULT 1, name VARCHAR(256));
