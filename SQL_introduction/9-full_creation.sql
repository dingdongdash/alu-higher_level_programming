-- Creates the table second_table and adds rows to it
-- Creates second_table if it does not already exist
CREATE TABLE IF NOT EXISTS second_table (id INT, name VARCHAR(256), score INT);
-- Adds the rows (1, John, 10), (2, Alex, 3), (3, Bob, 14), (4, George, 8)
INSERT INTO second_table (id, name, score) VALUES (1, 'John', 10), (2, 'Alex', 3), (3, 'Bob', 14), (4, 'George', 8);
