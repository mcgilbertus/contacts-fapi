import datetime

import pytest

from data.database import create_db_test_instance, db_instance
from data.repositories.contactos_repo import ContactosRepo
from domain.model.contactos import ContactoSinId


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
    OJO los ids son automáticos. Las pruebas asumen que se toman los valores 1, 2, 3
    porque la BD fue recreada completamente
    """
    repository = ContactosRepo()
    repository.agregar(db, ContactoSinId(nombre='Contacto1', direccion='dir1', telefonos='tel1', fecha_nac=datetime.date(1999, 8, 23)))
    repository.agregar(db, ContactoSinId(nombre='Contacto2', direccion='dir2'))
    repository.agregar(db, ContactoSinId(nombre='Contacto3'))

    return repository
