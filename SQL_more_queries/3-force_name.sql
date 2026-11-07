-- Creates a table called force_name in the current database
-- Creates force_name with a name column that cannot be NULL if the table does not already exist
CREATE TABLE IF NOT EXISTS force_name (id INT, name VARCHAR(256) NOT NULL);
