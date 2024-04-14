from data.database import Base
from sqlalchemy import Column, Integer, String, Date


class ContactoBd(Base):
    __tablename__ = 'contactos3'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(80), nullable=False)
    direccion = Column(String(120))
    telefonos = Column(String(50))
    fecha_nac = Column(Date)
