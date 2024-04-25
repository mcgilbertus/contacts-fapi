import datetime

import pytest

from data.database import create_db_test_instance, db_instance
from data.repositories.contactos_repo import ContactosRepo
from domain.model.contacto import Contacto


@pytest.fixture(scope='function', name='db')
def db_test():
    """Borra y recrea la base de datos"""
    create_db_test_instance()
    db_instance.drop_all()
    db_instance.create_all()
    return next(db_instance.get_db())


@pytest.fixture(scope='function', name='repo')
def inicializa_datos(db):
    """
    Agrega datos iniciales
    """
    db.begin()
    db.add(Contacto(id=1, nombre='Contacto1', direccion='dir1', telefonos='tel1', fecha_nac=datetime.date(1999, 8, 23)))
    db.add(Contacto(id=2, nombre='Contacto2', direccion='dir2'))
    db.add(Contacto(id=3, nombre='Contacto3'))
    db.commit()
    # inicializa y devuelve una instancia del repositorio
    return ContactosRepo()
