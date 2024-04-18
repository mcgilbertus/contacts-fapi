import datetime

import pytest
from fastapi.testclient import TestClient

import contactos_v1


# region Fixtures

@pytest.fixture(scope='module')
def test_client():
    return TestClient(contactos_v1.app)


@pytest.fixture(scope='function')
def inicializa_datos():
    contactos_v1.contactos = [
        contactos_v1.Contacto(id=1, nombre='Contacto1', direccion='dir1', telefonos='tel1',
                              fecha_nac=datetime.date(1999, 8, 23)),
        contactos_v1.Contacto(id=2, nombre='Contacto2', direccion='dir2'),
        contactos_v1.Contacto(id=3, nombre='Contacto3')
    ]

# endregion

# region endpoints

def test_getAll_devuelveLista(inicializa_datos, test_client):
    response = test_client.get("/contactos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(contactos_v1.contactos)
    # verifica que se recibieron todos los contactos almacenados, con los mismos valores
    for i, c in enumerate(data):
        assert busca_contacto_y_compara(c)


def test_getContacto_idCorrecto_devuelveContacto(inicializa_datos, test_client):
    id = 2
    response = test_client.get(f"/contactos/{id}")
    assert response.status_code == 200
    # obtiene un diccionario con los datos recibidos en json
    data = response.json()
    assert busca_contacto_y_compara(data)


def test_getContacto_idIncorrecto_devuelve404(inicializa_datos, test_client):
    id = 99
    response = test_client.get(f"/contactos/{id}")
    assert response.status_code == 404


def test_agregarContacto_todoBien_devuelveContacto(inicializa_datos, test_client):
    payload = {'nombre': 'nuevo contacto', 'direccion': 'nueva direccion'}
    response = test_client.post('/contactos', json=payload)
    assert response.status_code == 201
    data = response.json()
    assert busca_contacto_y_compara(data)


def test_agregarContacto_validationErrors_return422(inicializa_datos, test_client):
    payload = {'direccion': 'nueva direccion', 'fecha_nac': 'esto no es una fecha!'}
    response = test_client.post('/contactos', json=payload)
    # FastAPI returns code 422 on validation errors
    assert response.status_code == 422
    error_details = response.json()['detail']
    assert len(error_details) == 2
    assert error_details[0]['loc'][1] == 'nombre'
    assert error_details[0]['msg'] == 'Field required'
    assert error_details[1]['loc'][1] == 'fecha_nac'
    assert error_details[1]['msg'] == ('Input should be a valid date or datetime, '
                                       'invalid character in year')


def test_editarContacto_todoBien_devuelveContacto(inicializa_datos, test_client):
    payload = {'nombre': 'nuevo contacto', 'direccion': 'nueva direccion'}
    response = test_client.put('/contactos/1', json=payload)
    assert response.status_code == 200
    data = response.json()
    assert busca_contacto_y_compara(data)


def test_editarContacto_validationErrors_return422(inicializa_datos, test_client):
    payload = {'direccion': 'nueva direccion', 'fecha_nac': 'esto no es una fecha!'}
    response = test_client.put('/contactos/1', json=payload)
    # FastAPI returns code 422 on validation errors
    assert response.status_code == 422
    error_details = response.json()['detail']
    assert len(error_details) == 2
    assert error_details[0]['loc'][1] == 'nombre'
    assert error_details[0]['msg'] == 'Field required'
    assert error_details[1]['loc'][1] == 'fecha_nac'
    assert error_details[1]['msg'] == ('Input should be a valid date or datetime, '
                                       'invalid character in year')


def test_borrar_idCorrecto_devuelve204(inicializa_datos, test_client):
    id = 1
    response = test_client.delete(f"/contactos/{id}")
    assert response.status_code == 204
    # verifica que el contacto no exista mas en el almacenamiento
    assert next((x for x in contactos_v1.contactos if x.id == 1), None) is None


def test_borrar_idIncorrecto_devuelve404(inicializa_datos, test_client):
    id = 99
    response = test_client.delete(f"/contactos/{id}")
    assert response.status_code == 404


# endregion

# region helper functions

def busca_contacto_y_compara(datos: dict) -> bool:
    # crea una instancia de Contacto con los datos recibidos, para que Pydantic adapte los valores
    # a los tipos correctos
    cto_recibido = contactos_v1.Contacto(**{k: v for k, v in datos.items() if v is not None})
    # busca el contacto almacenado con el mismo id
    cto_almacenado = next((x for x in contactos_v1.contactos if x.id == cto_recibido.id), None)
    # compara los dos contactos propiedad por propiedad y devuelve true si no hay diferencias
    orig_values = cto_almacenado.model_dump()
    for k, v in cto_recibido.model_dump().items():
        if orig_values[k] != v:
            return False
    return True

# endregion
