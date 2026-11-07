-- Lists all the cities of California found in the database hbtn_0d_usa
-- Selects the id and name of the cities whose state is California using a subquery, sorted by id
SELECT id, name FROM cities WHERE state_id = (SELECT id FROM states WHERE name = 'California') ORDER BY id ASC;
