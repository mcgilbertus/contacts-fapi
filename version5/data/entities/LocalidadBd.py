from data.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class LocalidadBd(Base):
    __tablename__ = 'localidades'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(80), nullable=False)
    pais_id = Column(Integer, ForeignKey('paises.id'))

    pais = relationship('PaisBd')
