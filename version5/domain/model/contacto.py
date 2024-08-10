# contacto.py

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import composite, relationship, mapped_column, Mapped

from data.database import OrmBase
from domain.model.direccion import Direccion


class Contacto(OrmBase):
    __tablename__ = 'contactos'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(80), nullable=False)
    telefonos = Column(String(50))
    fecha_nac = Column(Date)
    nrodoc = Column(String(20))

    direccion: Mapped[Direccion] = composite(mapped_column('calle',String(80)),
                                             mapped_column('numero', Integer),
                                             mapped_column('piso', Integer),
                                             mapped_column('depto', String(10)),
                                             mapped_column('localidad_id', ForeignKey('localidades.id')))

    localidad = relationship('Localidad')
