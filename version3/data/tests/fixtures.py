import datetime

import pytest

from data import database
from data.database import Database, DB_TEST_CONNECTION
from data.repositories.contactos_repo import ContactosRepo
from domain.model.contactos import Contacto, ContactoSinId


@pytest.fixture(scope='function', name='repo')
def inicializa_datos():
    database.db_instance = Database(connection_string=DB_TEST_CONNECTION)
    database.db_instance.create_all()

    repository = ContactosRepo()
    repository.agregar(database.db_instance.get_db(),
                       ContactoSinId(nombre='Contacto1', direccion='dir1', telefonos='tel1',
                                     fecha_nac=datetime.date(1999, 8, 23)))
        Contacto(id=2, nombre='Contacto2', direccion='dir2'),
        Contacto(id=3, nombre='Contacto3')
    ]
    return repository
