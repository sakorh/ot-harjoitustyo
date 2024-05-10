from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class FEN(Base):
    __tablename__ = 'Fen'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    fen = Column(String(75), nullable=False)
