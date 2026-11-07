#!/usr/bin/python3
"""Deletes all the State objects whose name contains the letter a."""
import sys
from model_state import Base, State
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

if __name__ == "__main__":
    engine = create_engine("mysql+mysqldb://{}:{}@localhost:3306/{}".format(
        sys.argv[1], sys.argv[2], sys.argv[3]), pool_pre_ping=True)
    session = sessionmaker(bind=engine)()
    for state in session.query(State).filter(State.name.contains("a")).all():
        session.delete(state)
    session.commit()
    session.close()
