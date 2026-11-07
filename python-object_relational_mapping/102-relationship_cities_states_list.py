#!/usr/bin/python3
"""Lists all the City objects together with the name of their State."""
import sys
from relationship_state import Base, State
from relationship_city import City
from sqlalchemy import create_engine
from sqlalchemy.orm import joinedload, sessionmaker

if __name__ == "__main__":
    engine = create_engine("mysql+mysqldb://{}:{}@localhost:3306/{}".format(
        sys.argv[1], sys.argv[2], sys.argv[3]), pool_pre_ping=True)
    session = sessionmaker(bind=engine)()
    for city in session.query(City).options(
            joinedload(City.state)).order_by(City.id).all():
        print("{}: {} -> {}".format(city.id, city.name, city.state.name))
    session.close()
