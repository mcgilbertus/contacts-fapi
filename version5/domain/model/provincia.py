# provincia.py

from sqlalchemy import Column, Integer, String

from data.database import OrmBase


class Provincia(OrmBase):
    __tablename__ = 'provincias'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(80), nullable=False)
    pais = Column(String(50))
