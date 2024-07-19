from .base import Base, base
from sqlalchemy import Column, String

class Unit(Base, base):
    #units
    __tablename__ = "units"
    name = Column(String(30), nullable=False)
    mentor = Column(String(30))
