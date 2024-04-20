import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from contactos_v3 import app
from data.database import create_db_test_instance, db_instance
from data.entities.modelos_bd import ContactoBd


@pytest.fixture(scope='module')
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
def datos_test(db) -> list[ContactoBd]:
    datos = [
        ContactoBd(id=1, nombre='Contacto1', direccion='dir1', telefonos='tel1', fecha_nac=datetime.date(1999, 8, 23)),
        ContactoBd(id=2, nombre='Contacto2', direccion='dir2'),
        ContactoBd(id=3, nombre='Contacto3')
    ]
    db.add_all(datos)
    db.commit()
    return datos


