from data.database import Base
from sqlalchemy import Column, Integer, String


class ProvinciaBd(Base):
    __tablename__ = 'provincias'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(80), nullable=False)
    pais = Column(String(80), nullable=True)
