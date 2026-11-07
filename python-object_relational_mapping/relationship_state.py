#!/usr/bin/python3
"""Defines the State class linked to its cities and the Base of the pair."""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class State(Base):
    """Represents a row of the states table and the cities linked to it."""
    __tablename__ = "states"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(128), nullable=False)
    cities = relationship("City", back_populates="state",
                          cascade="all, delete-orphan", order_by="City.id",
                          lazy="joined")


import relationship_city  # noqa: E402,F401
