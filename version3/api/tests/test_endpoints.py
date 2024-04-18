from data.repositories.contactos_repo import ContactosRepo
from domain.model.contactos import Contacto
from fixtures import test_client, inicializa_datos as repo


# region endpoints
def test_getAll_devuelveLista(repo: ContactosRepo, test_client):
    response = test_client.get("/contactos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(repo.contactos)
    # verifica que se recibieron todos los contactos almacenados, con los mismos valores
    for i, c in enumerate(data):
        assert busca_contacto_y_compara(c, repo)


def test_getContacto_idCorrecto_devuelveContacto(repo: ContactosRepo, test_client):
    id = 2
    response = test_client.get(f"/contactos/{id}")
    assert response.status_code == 200
    # obtiene un diccionario con los datos recibidos en json
    data = response.json()
    assert busca_contacto_y_compara(data, repo)


def test_getContacto_idIncorrecto_devuelve404(repo: ContactosRepo, test_client):
    id = 99
    response = test_client.get(f"/contactos/{id}")
    assert response.status_code == 404


def test_agregarContacto_todoBien_devuelveContacto(repo: ContactosRepo, test_client):
    payload = {'nombre': 'nuevo contacto', 'direccion': 'nueva direccion'}
    response = test_client.post('/contactos', json=payload)
    assert response.status_code == 201
    data = response.json()
    assert busca_contacto_y_compara(data, repo)


def test_agregarContacto_validationErrors_return422(repo: ContactosRepo, test_client):
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


def test_editarContacto_todoBien_devuelveContacto(repo: ContactosRepo, test_client):
    payload = {'nombre': 'nuevo contacto', 'direccion': 'nueva direccion'}
    response = test_client.put('/contactos/1', json=payload)
    assert response.status_code == 200
    data = response.json()
    assert busca_contacto_y_compara(data, repo)


def test_editarContacto_validationErrors_return422(repo: ContactosRepo, test_client):
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


def test_borrar_idCorrecto_devuelve204(repo: ContactosRepo, test_client):
    id = 1
    response = test_client.delete(f"/contactos/{id}")
    assert response.status_code == 204
    # verifica que el contacto no exista mas en el almacenamiento
    assert next((x for x in repo.contactos if x.id == 1), None) is None


def test_borrar_idIncorrecto_devuelve404(repo: ContactosRepo, test_client):
    id = 99
    response = test_client.delete(f"/contactos/{id}")
    assert response.status_code == 404


# endregion

# region helper functions

def busca_contacto_y_compara(datos: dict, repo: ContactosRepo) -> bool:
    # crea una instancia de Contacto con los datos recibidos, para que Pydantic adapte los valores
    # a los tipos correctos
    cto_recibido = Contacto(**{k: v for k, v in datos.items() if v is not None})
    # busca el contacto almacenado con el mismo id
    cto_almacenado = repo.buscar_contacto(cto_recibido.id)[0]
    # compara los dos contactos propiedad por propiedad y devuelve true si no hay diferencias
    orig_values = cto_almacenado.model_dump()
    for k, v in cto_recibido.model_dump().items():
        if orig_values[k] != v:
            return False
    return True

# endregion
