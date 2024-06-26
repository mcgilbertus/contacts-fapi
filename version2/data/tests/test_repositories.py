import pytest

from data.repositories.contactos_repo import ContactosRepo
from domain.exceptions.NotFound import NotFoundError
from domain.model.contactos import Contacto, ContactoSinId
from fixtures import inicializa_datos as repo


# region get_all
def test_getAll_devuelveLista(repo: ContactosRepo):
    data = repo.get_all()
    assert len(data) == len(repo.contactos)
    # verifica que se recibieron todos los contactos almacenados, con los mismos valores
    for c in data:
        assert busca_contacto_y_compara(c, repo)

# endregion

# region get_by_id
def test_getById_idCorrecto_devuelveContacto(repo: ContactosRepo):
    data = repo.get_by_id(2)
    assert busca_contacto_y_compara(data, repo)


def test_getById_idIncorrecto_notFoundError(repo: ContactosRepo):
    with pytest.raises(NotFoundError):
        repo.get_by_id(99)

# endregion

# region agregar
def test_agregar_todoBien_devuelveContacto(repo: ContactosRepo):
    payload = ContactoSinId(**{'nombre': 'nuevo contacto', 'direccion': 'nueva direccion'})
    data = repo.agregar(payload)
    assert busca_contacto_y_compara(data, repo)

# endregion

# region editar
def test_editar_todoBien_devuelveContacto(repo: ContactosRepo):
    payload = ContactoSinId(**{'nombre': 'nuevo contacto', 'direccion': 'nueva direccion'})
    data = repo.editar(1, payload)
    assert busca_contacto_y_compara(data, repo)

# endregion

# region borrar
def test_borrar_idCorrecto_borraContacto(repo: ContactosRepo):
    repo.borrar(1)
    # verifica que el contacto no exista mas en el almacenamiento
    with pytest.raises(NotFoundError):
        repo.buscar_contacto(1)


def test_borrar_idIncorrecto_notFoundError(repo: ContactosRepo):
    with pytest.raises(NotFoundError):
        repo.borrar(99)

# endregion

# region helper functions
def busca_contacto_y_compara(cto: Contacto, repo: ContactosRepo) -> bool:
    # busca el contacto almacenado con el mismo id
    cto_almacenado = repo.buscar_contacto(cto.id)[0]
    # compara los dos contactos propiedad por propiedad y devuelve true si no hay diferencias
    orig_values = cto_almacenado.model_dump()
    for k, v in cto.model_dump().items():
        if orig_values[k] != v:
            return False
    return True
# endregion
