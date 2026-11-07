-- Lists all the cities of the database hbtn_0d_usa with the name of their state
-- Selects the city id, the city name and the state name, sorted by city id
SELECT cities.id, cities.name, states.name FROM cities INNER JOIN states ON cities.state_id = states.id ORDER BY cities.id ASC;
