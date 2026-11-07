# python-object_relational_mapping

Python - Object-relational mapping: scripts that talk to a MySQL server with `MySQLdb` and map tables to Python classes with `SQLAlchemy`.

| File | Description |
| --- | --- |
| `0-select_states.py` | Lists all states of the database `hbtn_0e_0_usa` sorted by `states.id`. |
| `1-filter_states.py` | Lists all states whose name starts with an uppercase `N`. |
| `2-my_filter_states.py` | Displays the states matching the name given as argument, building the query with `format`. |
| `3-my_safe_filter_states.py` | Displays the states matching the name given as argument, safe against SQL injection. |
| `4-cities_by_state.py` | Lists all cities of `hbtn_0e_4_usa` with the name of their state. |
| `5-filter_cities.py` | Lists, on one line, the cities of the state given as argument. |
| `model_state.py` | Defines the `State` class and the `Base` instance used by the SQLAlchemy scripts. |
| `7-model_state_fetch_all.py` | Lists all `State` objects of `hbtn_0e_6_usa`. |
| `8-model_state_fetch_first.py` | Prints the first `State` object, or `Nothing` when the table is empty. |
| `9-model_state_filter_a.py` | Lists the `State` objects whose name contains the letter `a`. |
| `10-model_state_my_get.py` | Prints the id of the `State` named like the argument, or `Not found`. |
| `11-model_state_insert.py` | Adds the `State` `Louisiana` and prints its new id. |
| `12-model_state_update_id_2.py` | Changes the name of the `State` with id 2 to `New Mexico`. |
| `13-model_state_delete_a.py` | Deletes all `State` objects whose name contains the letter `a`. |
| `model_city.py` | Defines the `City` class linked to the `cities` table. |
| `14-model_city_fetch_by_state.py` | Lists all `City` objects of `hbtn_0e_14_usa` as `<state name>: (<city id>) <city name>`. |

Every script takes the MySQL username, password and database name as arguments (the scripts that filter also take a state name) and connects to `localhost` on port `3306`.

All Python scripts are interpreted on Ubuntu 20.04 LTS with python3 (3.8.5), use `MySQLdb` (2.0.x) and `SQLAlchemy` (1.4.x), follow the pycodestyle (version 2.7.*) style and are executable.
