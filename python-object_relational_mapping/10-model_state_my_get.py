#!/usr/bin/python3
"""Prints the id of the State object named like the user argument."""
import sys
from model_state import Base, State
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

if __name__ == "__main__":
    engine = create_engine("mysql+mysqldb://{}:{}@localhost:3306/{}".format(
        sys.argv[1], sys.argv[2], sys.argv[3]), pool_pre_ping=True)
    session = sessionmaker(bind=engine)()
    state = session.query(State).filter(State.name == sys.argv[4]).first()
    if state is None:
        print("Not found")
    else:
        print(state.id)
    session.close()
