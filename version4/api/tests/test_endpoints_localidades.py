import pytest
from pydantic import BaseModel

from api.model.localidad_modelos import LocalidadDetailModel, LocalidadListModel
from data.repositories.localidades_repo import LocalidadesRepo
from domain.exceptions.NotFound import NotFoundError
from domain.model.localidad import Localidad
# es necesario importar db_test aunque no se use, para que se registre como fixture
from fixtures_api import test_client, db_test, datos_provincias, datos_localidades


# region endpoints
def test_getAll_devuelveLista(test_client, datos_provincias, datos_localidades):
    response = test_client.get("/localidades")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    # verifica que se recibieron todos los localidades almacenados, con los mismos valores
    for i, c in enumerate(data):
        almacenado = next((x for x in datos_localidades if x.id == c['id']), None)
        assert almacenado is not None
        assert almacenado.nombre == c['nombre']
        if 'provincia' in c:
            provincia = next((x for x in datos_provincias if x.nombre == c['provincia']), None)
            assert provincia is not None



def test_getLocalidad_idCorrecto_devuelveLocalidad(test_client, datos_provincias, datos_localidades):
    id = 2
    response = test_client.get(f"/localidades/{id}")
    assert response.status_code == 200
    # el dato recibido deberia ser un LocalidadDetailModel
    detail = response.json()
    loc = next((x for x in datos_localidades if x.id == detail['id']), None)
    assert loc is not None
    prov = next((x for x in datos_provincias if x.id == detail['provincia']['id']), None)
    assert prov is not None



def test_getLocalidad_idIncorrecto_devuelve404(test_client):
    id = 99
    response = test_client.get(f"/localidades/{id}")
    assert response.status_code == 404


def test_agregarLocalidad_todoBien_devuelveLocalidad(test_client, datos_provincias, datos_localidades):
    payload = {'nombre': 'mi localidad', 'provincia_id': 1}
    response = test_client.post('/localidades', json=payload)
    assert response.status_code == 201
    detail = response.json()
    assert detail['nombre'] == 'mi localidad'
    assert detail['provincia']['id'] == 1
    prov = next((x for x in datos_provincias if x.id == detail['provincia']['id']), None)
    assert prov is not None


def test_agregarLocalidad_validationErrors_return422(test_client, datos_provincias, datos_localidades):
    payload = {'provincia_id': 1}
    response = test_client.post('/localidades', json=payload)
    # FastAPI returns code 422 on validation errors
    assert response.status_code == 422
    error_details = response.json()['detail']
    assert len(error_details) == 1
    assert error_details[0]['loc'][1] == 'nombre'
    assert error_details[0]['msg'] == 'Field required'


def test_agregarLocalidad_provinciaInexistente_return422(test_client, datos_provincias, datos_localidades):
    payload = {'nombre':'nueva loc', 'provincia_id': 99}
    response = test_client.post('/localidades', json=payload)
    # FastAPI returns code 422 on validation errors
    assert response.status_code == 409
    error_details = response.json()['detail']
    assert error_details.startswith('Error 547')


def test_editarLocalidad_todoBien_devuelveLocalidad(test_client, datos_provincias, datos_localidades):
    payload = {'nombre': 'mi localidad', 'provincia': 1}
    response = test_client.put('/localidades/1', json=payload)
    assert response.status_code == 200
    data = response.json()
    loc = next((x for x in datos_localidades if x.id == data['id']), None)
    assert loc is not None
    assert loc.nombre == 'mi localidad'
    prov = next((x for x in datos_provincias if x.id == data['provincia']['id']), None)
    assert prov is not None


def test_editarLocalidad_validationErrors_return422(test_client, datos_provincias, datos_localidades):
    payload = {'provincia_id': 1}
    response = test_client.put('/localidades/1', json=payload)
    # FastAPI returns code 422 on validation errors
    assert response.status_code == 422
    error_details = response.json()['detail']
    assert len(error_details) == 1
    assert error_details[0]['loc'][1] == 'nombre'
    assert error_details[0]['msg'] == 'Field required'


def test_borrar_idCorrecto_devuelve204(test_client, datos_provincias, datos_localidades, db):
    id = 1
    response = test_client.delete(f"/localidades/{id}")
    assert response.status_code == 204
    # verifica que el localidad no exista mas en el almacenamiento
    repo = LocalidadesRepo()
    with pytest.raises(NotFoundError):
        repo.get_by_id(db, 1)


def test_borrar_idIncorrecto_devuelve404(test_client, datos_provincias, datos_localidades):
    id = 99
    response = test_client.delete(f"/localidades/{id}")
    assert response.status_code == 404

# endregion
