#!/usr/bin/python3
"""
    learners table modeling
    import Base instance of metadata to hold database schema
"""

from .base import base, Base, DateTime
from sqlalchemy import Column, String,Numeric, Integer, ForeignKey

class Enroll(Base, base):

    """"""
    __tablename__ = "enrolls"
    learnerId = Column(String(60), ForeignKey("learners.id"))
    unitId = Column(String(60), ForeignKey("units.id"))
    pprogress = Column(Integer, nullable=False, default=0)
    scheduled = Column(Integer, default=0)
    S_time = Column(DateTime())
    lastS = Column(Integer, default=0)
