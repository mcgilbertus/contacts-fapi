from datetime import datetime

import pytest

from data.repositories.contactos_repo import ContactosRepo
from domain.exceptions.NotFound import NotFoundError
from domain.model.contacto import Contacto
from domain.model.direccion import Direccion
# es necesario importar db_test aunque no se use, para que se registre como fixture
from fixtures_api import test_client, db_test, datos_contactos


# region endpoints
def test_getAll_devuelveLista(test_client, datos_contactos):
    response = test_client.get("/contactos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    # verifica que se recibieron todos los contactos almacenados, con los mismos valores
    for c in data:
        cto = next((x for x in datos_contactos if x.id == c['id']), None)
        assert cto is not None
        assert c['nombre'] == cto.nombre
        assert c.get('telefonos', None) == cto.telefonos
        if c.get('fecha_nac', None) is not None:
            assert datetime.strptime(c['fecha_nac'], '%Y-%m-%d').date() == cto.fecha_nac
        else:
            assert cto.fecha_nac is None
        assert c.get('direccion', None) == direccion_str(cto.direccion)


def test_getContacto_idCorrecto_devuelveContacto(test_client, datos_contactos):
    id = 2
    response = test_client.get(f"/contactos/{id}")
    assert response.status_code == 200
    # obtiene un diccionario con los datos recibidos en json
    data = response.json()
    assert busca_contacto_y_compara(datos_contactos, data)


def test_getContacto_idIncorrecto_devuelve404(test_client, datos_contactos):
    id = 99
    response = test_client.get(f"/contactos/{id}")
    assert response.status_code == 404


def test_agregarContacto_todoBien_devuelveContacto(test_client, datos_contactos):
    payload = {'nombre': 'nuevo contacto', 'direccion': {'calle': 'nueva direccion'}}
    response = test_client.post('/contactos', json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data['nombre'] == 'nuevo contacto'
    assert data['direccion']['calle'] == 'nueva direccion'
    assert data['id'] is not None


def test_agregarContacto_validationErrors_return422(test_client, datos_contactos):
    payload = {'direccion': {'calle': 'nueva direccion'}, 'fecha_nac': 'esto no es una fecha!'}
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


def test_editarContacto_todoBien_devuelveContacto(test_client, datos_contactos):
    payload = {'nombre': 'nuevo contacto', 'direccion': {'calle': 'nueva direccion'}}
    response = test_client.put('/contactos/1', json=payload)
    assert response.status_code == 200
    data = response.json()
    assert busca_contacto_y_compara(datos_contactos, data)


def test_editarContacto_validationErrors_return422(test_client, datos_contactos):
    payload = {'direccion': {'calle': 'nueva direccion'}, 'fecha_nac': 'esto no es una fecha!'}
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


def test_borrar_idCorrecto_devuelve204(test_client, datos_contactos, db):
    id = 1
    response = test_client.delete(f"/contactos/{id}")
    assert response.status_code == 204
    # verifica que el contacto no exista mas en el almacenamiento
    repo = ContactosRepo()
    with pytest.raises(NotFoundError):
        repo.get_by_id(db, 1)


def test_borrar_idIncorrecto_devuelve404(test_client, datos_contactos):
    id = 99
    response = test_client.delete(f"/contactos/{id}")
    assert response.status_code == 404


# endregion


# region helper functions

def busca_contacto_y_compara(datos_contactos: list[Contacto], datos: dict) -> bool:
    # busca el contacto almacenado con el mismo id
    cto_almacenado = next((x for x in datos_contactos if x.id == datos['id']), None)
    assert cto_almacenado is not None

    direccion = Direccion(**datos.pop('direccion', {}))
    cto_recibido = Contacto(**{k: v for k, v in datos.items() if v is not None})
    cto_recibido.direccion = direccion

    for k, v in {k: v for k, v in cto_recibido.__dict__.items() if not k.startswith('_')}.items():
        if getattr(cto_almacenado, k) != v:
            return False
    return True


def direccion_str(d: Direccion) -> str:
    if d.calle is None:
        return None
    result = f'{d.calle}'
    if d.numero is not None:
        result += f' {d.numero}'
        if d.piso is not None:
            result += f', {d.piso}'
            if d.depto is not None:
                result += f' {d.depto}'
    return result

# endregion
