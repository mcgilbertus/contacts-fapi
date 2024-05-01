import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from data.repositories.contactos_repo import ContactosRepo
from domain.exceptions.NotFound import NotFoundError
from domain.model.contacto import Contacto
from fixtures_data import inicializa_datos_contacto as repo, db_test as db


# region get_all
def test_getAll_devuelveLista(db: Session, repoContacto: ContactosRepo):
    data = repoContacto.get_all(db)
    assert len(data) == 3
    # verifica que se recibieron todos los contactos almacenados, con los mismos valores
    for c in data:
        assert busca_contacto_y_compara(db, c, repoContacto)


# endregion

# region get_by_id
def test_getById_idCorrecto_devuelveContacto(db: Session, repoContacto: ContactosRepo):
    data = repoContacto.get_by_id(db, 2)
    assert busca_contacto_y_compara(db, data, repoContacto)


def test_getById_idIncorrecto_notFoundError(db: Session, repoContacto: ContactosRepo):
    with pytest.raises(NotFoundError):
        repoContacto.get_by_id(db, 99)


# endregion

# region agregar
def test_agregar_todoBien_devuelveContacto(db: Session, repoContacto: ContactosRepo):
    payload = Contacto(nombre= 'nuevo contacto', direccion= 'nueva direccion')
    data = repoContacto.agregar(db, payload)
    assert busca_contacto_y_compara(db, data, repoContacto)


# end region

# region editar
def test_editar_todoBien_devuelveContacto(db: Session, repoContacto: ContactosRepo):
    payload = {'nombre': 'nuevo contacto', 'direccion': 'nueva direccion'}
    data = repoContacto.editar(db, 1, payload)
    assert busca_contacto_y_compara(db, data, repoContacto)


# endregion

# region borrar
def test_borrar_idCorrecto_borraContacto(db: Session, repoContacto: ContactosRepo):
    repoContacto.borrar(db, 1)
    # verifica que el contacto no exista mas en el almacenamiento
    # no se puede usar get_by_id porque el contacto esta en memoria
    assert db.scalar(text('SELECT id FROM Contactos WHERE id = 1')) == None


def test_borrar_idIncorrecto_notFoundError(db: Session, repoContacto: ContactosRepo):
    with pytest.raises(NotFoundError):
        repoContacto.borrar(db, 99)


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
