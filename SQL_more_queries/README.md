# SQL - More queries

More MySQL: creating users and privileges, constraints, foreign keys, subqueries and joins.

Each `.sql` file is piped to the MySQL client, for example:

```
cat 0-privileges.sql | mysql -hlocalhost -uroot -p
cat 8-cities_of_california_subquery.sql | mysql -hlocalhost -uroot -p hbtn_0d_usa
```

Tasks 10 to 16 use the `hbtn_0d_tvshows` database, imported from the `hbtn_0d_tvshows.sql` dump provided with the project (not included in this repository).

| File | Task |
| --- | --- |
| `0-privileges.sql` | List the privileges of `user_0d_1` and `user_0d_2` |
| `1-create_user.sql` | Create `user_0d_1` with all privileges |
| `2-create_read_user.sql` | Create `hbtn_0d_2` and `user_0d_2` with SELECT only |
| `3-force_name.sql` | Create `force_name` with a name that cannot be NULL |
| `4-never_empty.sql` | Create `id_not_null` with an id that defaults to 1 |
| `5-unique_id.sql` | Create `unique_id` with a unique id |
| `6-states.sql` | Create `hbtn_0d_usa` and the table `states` |
| `7-cities.sql` | Create the table `cities` with a foreign key to `states` |
| `8-cities_of_california_subquery.sql` | List the cities of California with a subquery |
| `9-cities_by_state_join.sql` | List all cities with their state using a join |
| `10-genre_id_by_show.sql` | List shows with their genre ids |
| `11-genre_id_all_shows.sql` | List all shows with their genre ids, NULL if none |
| `12-no_genre.sql` | List the shows without a genre |
| `13-count_shows_by_genre.sql` | Count the shows of each genre |
| `14-my_genres.sql` | List the genres of Dexter |
| `15-comedy_only.sql` | List the Comedy shows |
| `16-shows_by_genre.sql` | List all shows with their genre names |
