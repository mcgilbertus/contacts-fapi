import pytest

from api.model.provincia_modelos import ProvinciaDetailModel
from data.repositories.provincias_repo import ProvinciasRepo
from domain.exceptions.NotFound import NotFoundError
from domain.model.provincia import Provincia
# es necesario importar db_test aunque no se use, para que se registre como fixture
from fixtures_api import test_client, datos_provincias, db_test


# region endpoints
def test_getAll_devuelveLista(test_client, datos_provincias):
    response = test_client.get("/provincias")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    # verifica que se recibieron todos los provincias almacenados, con los mismos valores
    for i, c in enumerate(data):
        assert busca_provincia_y_compara(datos_provincias, c)


def test_getProvincia_idCorrecto_devuelveProvincia(test_client, datos_provincias):
    id = 2
    response = test_client.get(f"/provincias/{id}")
    assert response.status_code == 200
    # obtiene un diccionario con los datos recibidos en json
    data = response.json()
    assert busca_provincia_y_compara(datos_provincias, data)


def test_getProvincia_idIncorrecto_devuelve404(test_client, datos_provincias):
    id = 99
    response = test_client.get(f"/provincias/{id}")
    assert response.status_code == 404


def test_agregarProvincia_todoBien_devuelveProvincia(test_client, datos_provincias):
    payload = {'nombre': 'mi provincia', 'pais': 'mi pais'}
    response = test_client.post('/provincias', json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data['nombre'] == 'mi provincia'
    assert data['pais'] == 'mi pais'
    assert data['id'] is not None


def test_agregarProvincia_validationErrors_return422(test_client, datos_provincias):
    payload = {'pais': 123}
    response = test_client.post('/provincias', json=payload)
    # FastAPI returns code 422 on validation errors
    assert response.status_code == 422
    error_details = response.json()['detail']
    assert len(error_details) == 2
    assert error_details[0]['loc'][1] == 'nombre'
    assert error_details[0]['msg'] == 'Field required'
    assert error_details[1]['loc'][1] == 'pais'
    assert error_details[1]['msg'] == ('Input should be a valid string')


def test_editarProvincia_todoBien_devuelveProvincia(test_client, datos_provincias):
    payload = {'nombre': 'mi provincia', 'pais': 'mi pais'}
    response = test_client.put('/provincias/1', json=payload)
    assert response.status_code == 200
    data = response.json()
    assert busca_provincia_y_compara(datos_provincias, data)


def test_editarProvincia_validationErrors_return422(test_client, datos_provincias):
    payload = {'pais': 'Argentina'}
    response = test_client.put('/provincias/1', json=payload)
    # FastAPI returns code 422 on validation errors
    assert response.status_code == 422
    error_details = response.json()['detail']
    assert len(error_details) == 1
    assert error_details[0]['loc'][1] == 'nombre'
    assert error_details[0]['msg'] == 'Field required'


def test_borrar_idCorrecto_devuelve204(test_client, datos_provincias, db):
    id = 1
    response = test_client.delete(f"/provincias/{id}")
    assert response.status_code == 204 
    # verifica que el provincia no exista mas en el almacenamiento
    repo = ProvinciasRepo()
    with pytest.raises(NotFoundError):
        repo.get_by_id(db, 1)


def test_borrar_idIncorrecto_devuelve404(test_client, datos_provincias):
    id = 99
    response = test_client.delete(f"/provincias/{id}")
    assert response.status_code == 404


# endregion

# region helper functions

def busca_provincia_y_compara(datos_provincias:list[Provincia], datos: dict) -> bool:
    # crea una instancia de ProvinciaModel con los datos recibidos, para que Pydantic adapte
    #  los valores (que salen como string en el json) a los tipos correctos
    recibido = ProvinciaDetailModel(**{k: v for k, v in datos.items() if v is not None})
    # busca el provincia almacenado con el mismo id
    almacenado = next((x for x in datos_provincias if x.id == recibido.id), None)
    # compara los dos provincias propiedad por propiedad y devuelve true si no hay diferencias
    for k, v in recibido.model_dump(exclude_unset=True).items():
        if getattr(almacenado, k) != v:
            return False
    return True

# endregion
