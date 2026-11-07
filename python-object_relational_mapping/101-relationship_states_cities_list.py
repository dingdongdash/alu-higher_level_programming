#!/usr/bin/python3
"""Lists all the State objects and the City objects linked to each of them."""
import sys
from relationship_state import Base, State
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

if __name__ == "__main__":
    engine = create_engine("mysql+mysqldb://{}:{}@localhost:3306/{}".format(
        sys.argv[1], sys.argv[2], sys.argv[3]), pool_pre_ping=True)
    session = sessionmaker(bind=engine)()
    for state in session.query(State).order_by(State.id).all():
        print("{}: {}".format(state.id, state.name))
        for city in sorted(state.cities, key=lambda city: city.id):
            print("\t{}: {}".format(city.id, city.name))
    session.close()
