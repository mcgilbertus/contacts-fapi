import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from api.model.contacto_modelos import ContactoSinIdModel
from data.repositories.contactos_repo import ContactosRepo
from domain.exceptions.NotFound import NotFoundError
from domain.model.contacto import Contacto
from fixtures_data import inicializa_datos as repo, db_test as db


# region get_all
def test_getAll_devuelveLista(db: Session, repo: ContactosRepo):
    data = repo.get_all(db)
    assert len(data) == 3
    # verifica que se recibieron todos los contactos almacenados, con los mismos valores
    for c in data:
        assert busca_contacto_y_compara(db, c, repo)


# endregion

# region get_by_id
def test_getById_idCorrecto_devuelveContacto(db: Session, repo: ContactosRepo):
    data = repo.get_by_id(db, 2)
    assert busca_contacto_y_compara(db, data, repo)


def test_getById_idIncorrecto_notFoundError(db: Session, repo: ContactosRepo):
    with pytest.raises(NotFoundError):
        repo.get_by_id(db, 99)


# endregion

# region agregar
def test_agregar_todoBien_devuelveContacto(db: Session, repo: ContactosRepo):
    payload = Contacto(nombre= 'nuevo contacto', direccion= 'nueva direccion')
    data = repo.agregar(db, payload)
    assert busca_contacto_y_compara(db, data, repo)


# end region

# region editar
def test_editar_todoBien_devuelveContacto(db: Session, repo: ContactosRepo):
    payload = {'nombre': 'nuevo contacto', 'direccion': 'nueva direccion'}
    data = repo.editar(db, 1, payload)
    assert busca_contacto_y_compara(db, data, repo)


# endregion

# region borrar
def test_borrar_idCorrecto_borraContacto(db: Session, repo: ContactosRepo):
    repo.borrar(db, 1)
    # verifica que el contacto no exista mas en el almacenamiento
    # no se puede usar get_by_id porque el contacto esta en memoria
    assert db.scalar(text('SELECT id FROM Contactos WHERE id = 1')) == None


def test_borrar_idIncorrecto_notFoundError(db: Session, repo: ContactosRepo):
    with pytest.raises(NotFoundError):
        repo.borrar(db, 99)


# endregion


# region helper functions

def busca_contacto_y_compara(bd: Session, cto: Contacto, repo: ContactosRepo) -> bool:
    # busca el contacto almacenado con el mismo id
    cto_almacenado = repo.get_by_id(bd, cto.id)
    # compara los dos contactos propiedad por propiedad y devuelve true si no hay diferencias
    orig_values = cto_almacenado.__dict__
    for k, v in cto.__dict__.items():
        if orig_values[k] != v:
            return False
    return True

# endregion
