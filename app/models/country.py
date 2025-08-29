from sqlalchemy import Column, Integer, String
from app.database.session import Base

class Country(Base):
    __tablename__ = "countries"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    name = Column(String, unique=True)
    flag_url = Column(String, nullable=True)
