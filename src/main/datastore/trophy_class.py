import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Trophy(Base):
    __tablename__ = 'trophy'

    sender_id = Column(String, nullable=False, primary_key=True)
    recipient_id = Column(String, nullable=False, primary_key=True)
    reason = Column(String)
    creation_timestamp = Column(DateTime, nullable=False, primary_key=True, default=datetime.datetime.utcnow)