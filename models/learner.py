#!/usr/bin/python3
"""
    learners table modeling
    import Base instance of metadata to hold database schema
"""

from .base import base, Base
from sqlalchemy import Table, Column, String,Numeric

class Learner(Base, base):

    """customer"""
    __tablename__ = "learners"
    name = Column(String(35), nullable=False)
    username = Column(String(25), nullable=False, unique=True)
    password = Column(String(15), nullable=False)
    email = Column(String(35), nullable=False, unique=True)
    phone = Column(String(18), nullable=False, unique=True)
    imgURL = Column(String(60))
