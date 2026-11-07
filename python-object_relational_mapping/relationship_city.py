#!/usr/bin/python3
"""Defines the City class mapped to the cities table and linked to a state."""
from relationship_state import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class City(Base):
    """Represents a row of the cities table and the state it belongs to."""
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(128), nullable=False)
    state_id = Column(Integer, ForeignKey("states.id"), nullable=False)
    state = relationship("State", back_populates="cities")
