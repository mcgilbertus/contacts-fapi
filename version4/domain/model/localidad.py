# localidad.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from data.database import OrmBase


class Localidad(OrmBase):
    __tablename__ = 'localidades'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(80), nullable=False)
    provincia_id = Column(Integer, ForeignKey('provincias.id'))

    provincia = relationship('Provincia')
