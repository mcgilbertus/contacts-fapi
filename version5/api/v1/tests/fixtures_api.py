import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from data.database import db_instance, connect_to_test
from contactos_v5 import app
from domain.model.contacto import Contacto
from domain.model.direccion import Direccion
from domain.model.localidad import Localidad
from domain.model.provincia import Provincia


@pytest.fixture(scope='package')
def test_client():
    return TestClient(app)


@pytest.fixture(scope='function', name='db')
def db_test() -> Session:
    """Borra y recrea la base de datos"""
    connect_to_test()
    db_instance.drop_all()
    db_instance.create_all()
    return next(db_instance.get_db())


@pytest.fixture(scope='function')
def datos_contactos(db) -> list[Contacto]:
    contactos = [
        Contacto(id=1, nombre='Contacto1', direccion=Direccion(calle="Cucha Cucha", numero=123),
                 telefonos='tel1', fecha_nac=datetime.date(1999, 8, 23)),
        Contacto(id=2, nombre='Contacto2', direccion=Direccion(calle="calle cto 2", numero=456,
                                                               piso=1, depto='A')),
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


@pytest.fixture(scope='function')
def datos_localidades(db) -> list[Localidad]:
    localidades = [
        Localidad(id=1, nombre='Loc1', provincia_id=1),
        Localidad(id=2, nombre='Loc2', provincia_id=1),
        Localidad(id=3, nombre='Loc3')
    ]

    db.add_all(localidades)
    db.commit()
    return localidades
