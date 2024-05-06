# domain.model.contacto.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import composite, relationship

from data.database import OrmBase
from domain.model.direccion import Direccion


class Contacto(OrmBase):
    __tablename__ = 'contactos'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(80), nullable=False)
    telefonos = Column(String(50))
    fecha_nac = Column(Date)

    # campos para la direccion
    calle = Column(String(80))
    numero = Column(Integer)
    piso = Column(Integer)
    depto = Column(String(10))
    localidad_id = Column(Integer, ForeignKey('localidades.id'))
    direccion = composite(Direccion, calle, numero, piso, depto, localidad_id)

    localidad = relationship('Localidad')
