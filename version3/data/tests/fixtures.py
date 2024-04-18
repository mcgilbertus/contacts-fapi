import datetime

import pytest

from data.repositories.contactos_repo import ContactosRepo
from domain.model.contactos import Contacto


@pytest.fixture(scope='function', name='repo')
def inicializa_datos():
    repository = ContactosRepo()
    repository.contactos = [
        Contacto(id=1, nombre='Contacto1', direccion='dir1', telefonos='tel1',
                 fecha_nac=datetime.date(1999, 8, 23)),
        Contacto(id=2, nombre='Contacto2', direccion='dir2'),
        Contacto(id=3, nombre='Contacto3')
    ]
    return repository
