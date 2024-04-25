# domain.model.contacto.py
from sqlalchemy import Column, Integer, String, Date

from data.database import OrmBase


class Contacto(OrmBase):
    __tablename__ = 'contactos'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(80), nullable=False)
    direccion = Column(String(120))
    telefonos = Column(String(50))
    fecha_nac = Column(Date)
