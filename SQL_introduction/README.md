# SQL - Introduction

Introduction to SQL with MySQL: scripts that create, list and delete databases and tables, then insert, query, update and delete rows.

Each `.sql` file is piped to the MySQL client, for example:

```
cat 0-list_databases.sql | mysql -hlocalhost -uroot -p
cat 6-list_values.sql | mysql -hlocalhost -uroot -p hbtn_0c_0
```

| File | Task |
| --- | --- |
| `0-list_databases.sql` | List all databases |
| `1-create_database_if_missing.sql` | Create the database `hbtn_0c_0` if missing |
| `2-remove_database.sql` | Delete the database `hbtn_0c_0` if it exists |
| `3-list_tables.sql` | List all tables of a database |
| `4-first_table.sql` | Create the table `first_table` |
| `5-full_table.sql` | Print the full description of `first_table` |
| `6-list_values.sql` | List all rows of `first_table` |
| `7-insert_value.sql` | Insert a row in `first_table` |
| `8-count_89.sql` | Count the rows with `id = 89` |
| `9-full_creation.sql` | Create `second_table` and add rows |
| `10-top_score.sql` | List records by best score |
| `11-best_score.sql` | Select records with a score >= 10 |
| `12-no_cheating.sql` | Update the score of Bob |
| `13-change_class.sql` | Remove records with a score <= 5 |
| `14-average.sql` | Compute the score average |
| `15-groups.sql` | Count records per score |
| `16-no_link.sql` | List records that have a name |
