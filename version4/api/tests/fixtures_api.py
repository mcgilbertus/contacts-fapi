import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from contactos_v4 import app
from data.database import create_db_test_instance, db_instance
from domain.model.contacto import Contacto
from domain.model.localidad import Localidad
from domain.model.provincia import Provincia


@pytest.fixture(scope='package')
def test_client():
    return TestClient(app)


@pytest.fixture(scope='function', name='db')
def db_test() -> Session:
    """Borra y recrea la base de datos"""
    create_db_test_instance()
    db_instance.drop_all()
    db_instance.create_all()
    return next(db_instance.get_db())


@pytest.fixture(scope='function')
def datos_contactos(db) -> list[Contacto]:
    contactos = [
        Contacto(id=1, nombre='Contacto1', direccion='dir1', telefonos='tel1', fecha_nac=datetime.date(1999, 8, 23)),
        Contacto(id=2, nombre='Contacto2', direccion='dir2'),
        Contacto(id=3, nombre='Contacto3')
    ]
    db.add_all(contactos)
    db.commit()
    return contactos


@pytest.fixture(scope='function')
def datos_provincias(db) -> list[Provincia]:
    provincias = [
        Provincia(id=1, nombre='Provincia1', pais='Pais1'),
        Provincia(id=2, nombre='Provincia2', pais='Pais2'),
        Provincia(id=3, nombre='Provincia3')
    ]

    db.add_all(provincias)
    db.commit()
    return provincias
