-- Creates a table called unique_id in the current database
-- Creates unique_id with a unique id column that defaults to 1 if the table does not already exist
CREATE TABLE IF NOT EXISTS unique_id (id INT DEFAULT 1 UNIQUE, name VARCHAR(256));
