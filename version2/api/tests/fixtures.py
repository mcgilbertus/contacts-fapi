import datetime

import pytest
from fastapi.testclient import TestClient

from api.controllers import contactos_api
from contactos_v2 import app
from domain.model.contactos import Contacto


@pytest.fixture(scope='module')
def test_client():
    return TestClient(app)


@pytest.fixture(scope='function', name='repo')
def inicializa_datos():
    repository = contactos_api.repo
    repository.contactos = [
        Contacto(id=1, nombre='Contacto1', direccion='dir1', telefonos='tel1',
                 fecha_nac=datetime.date(1999, 8, 23)),
        Contacto(id=2, nombre='Contacto2', direccion='dir2'),
        Contacto(id=3, nombre='Contacto3')
    ]
    return repository
