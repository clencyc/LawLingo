from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime
from app.database.session import Base

from sqlalchemy import ForeignKey, JSON
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    avatar = Column(String, nullable=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    total_xp = Column(Integer, default=0)
    current_level = Column(Integer, default=1)
    current_country = Column(String, ForeignKey("countries.code"), nullable=True)
    unlocked_countries = Column(JSON, default=list)
    current_streak = Column(Integer, default=0)
    learning_preferences = Column(JSON, default=dict)
    notification_settings = Column(JSON, default=dict)