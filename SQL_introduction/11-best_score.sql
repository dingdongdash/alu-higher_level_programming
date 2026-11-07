-- Lists all records of second_table with a score >= 10
-- Selects score then name, highest score first
SELECT score, name FROM second_table WHERE score >= 10 ORDER BY score DESC;
