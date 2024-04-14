from data.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class DireccionBd(Base):
    nombre = Column(String(80), nullable=False)
    numero = Column(Integer, nullable=True)
    piso = Column(Integer, nullable=True)
    depto = Column(String(10), nullable=True)
    localidad_id = Column(Integer, ForeignKey('localidades.id'))

    localidad = relationship('LocalidadBd')
