-- Lists all records of second_table that have a name value
-- Selects score then name, skipping NULL and empty names, highest score first
SELECT score, name FROM second_table WHERE name IS NOT NULL AND name != '' ORDER BY score DESC;
