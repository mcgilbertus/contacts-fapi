import datetime

import pytest

from data.database import create_db_test_instance, db_instance
from data.repositories.contactos_repo import ContactosRepo
from data.repositories.localidades_repo import LocalidadesRepo
from data.repositories.provincias_repo import ProvinciasRepo
from domain.model.contacto import Contacto
from domain.model.localidad import Localidad
from domain.model.provincia import Provincia


@pytest.fixture(scope='function', name='db')
def db_test():
    """Borra y recrea la base de datos"""
    create_db_test_instance()
    db_instance.drop_all()
    db_instance.create_all()
    return next(db_instance.get_db())


@pytest.fixture(scope='function', name='repoContacto')
def inicializa_datos_contacto(db):
    """
    Agrega datos iniciales
    """
    db.add(Contacto(id=1, nombre='Contacto1', direccion='dir1', telefonos='tel1', fecha_nac=datetime.date(1999, 8, 23)))
    db.add(Contacto(id=2, nombre='Contacto2', direccion='dir2'))
    db.add(Contacto(id=3, nombre='Contacto3'))
    db.commit()
    return ContactosRepo()


@pytest.fixture(scope='function', name='repoProvincia')
def inicializa_datos_provincia(db):
    """
    Agrega datos iniciales
    """
    db.add(Provincia(id=1, nombre='Provincia1', pais='Pais1'))
    db.add(Provincia(id=2, nombre='Provincia2', pais='Pais2'))
    db.add(Provincia(id=3, nombre='Provincia3'))
    db.commit()
    return ProvinciasRepo()


@pytest.fixture(scope='function', name='repoLocalidad')
def inicializa_datos_localidad(db):
    """
    Agrega datos iniciales
    """
    prov1 = Provincia(id=1, nombre='Provincia1', pais='Pais1')
    db.add(prov1)
    prov2 = Provincia(id=2, nombre='Provincia2', pais='Pais2')
    db.add(prov2)
    db.add(Localidad(id=1, nombre='Loc1', provincia_id=prov1.id))
    db.add(Localidad(id=2, nombre='Loc2', provincia_id=prov2.id))
    db.add(Localidad(id=3, nombre='Loc3'))
    db.commit()
    return LocalidadesRepo()
