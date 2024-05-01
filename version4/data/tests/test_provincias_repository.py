import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from data.repositories.provincias_repo import ProvinciasRepo
from domain.exceptions.NotFound import NotFoundError
from domain.model.provincia import Provincia
from fixtures_data import inicializa_datos_provincia as repo, db_test as db


# region get_all
def test_getAll_devuelveLista(db: Session, repoProvincia: ProvinciasRepo):
    data = repoProvincia.get_all(db)
    assert len(data) == 3
    # verifica que se recibieron todos los provincias almacenados, con los mismos valores
    for c in data:
        assert busca_provincia_y_compara(db, c, repoProvincia)


# endregion

# region get_by_id
def test_getById_idCorrecto_devuelveProvincia(db: Session, repoProvincia: ProvinciasRepo):
    data = repoProvincia.get_by_id(db, 2)
    assert busca_provincia_y_compara(db, data, repoProvincia)


def test_getById_idIncorrecto_notFoundError(db: Session, repoProvincia: ProvinciasRepo):
    with pytest.raises(NotFoundError):
        repoProvincia.get_by_id(db, 99)


# endregion

# region agregar
def test_agregar_todoBien_devuelveProvincia(db: Session, repoProvincia: ProvinciasRepo):
    payload = Provincia(nombre= 'nuevo provincia', pais= 'Pais1')
    data = repoProvincia.agregar(db, payload)
    assert busca_provincia_y_compara(db, data, repoProvincia)


# end region

# region editar
def test_editar_todoBien_devuelveProvincia(db: Session, repoProvincia: ProvinciasRepo):
    payload = {'nombre': 'nuevo provincia', 'direccion': 'nueva direccion'}
    data = repoProvincia.editar(db, 1, payload)
    assert busca_provincia_y_compara(db, data, repoProvincia)


# endregion

# region borrar
def test_borrar_idCorrecto_borraProvincia(db: Session, repoProvincia: ProvinciasRepo):
    repoProvincia.borrar(db, 1)
    # verifica que el provincia no exista mas en el almacenamiento
    # no se puede usar get_by_id porque el provincia esta en memoria
    assert db.scalar(text('SELECT id FROM Provincias WHERE id = 1')) == None


def test_borrar_idIncorrecto_notFoundError(db: Session, repoProvincia: ProvinciasRepo):
    with pytest.raises(NotFoundError):
        repoProvincia.borrar(db, 99)


# endregion


# region helper functions

def busca_provincia_y_compara(bd: Session, cto: Provincia, repo: ProvinciasRepo) -> bool:
    # busca el provincia almacenado con el mismo id
    cto_almacenado = repo.get_by_id(bd, cto.id)
    # compara los dos provincias propiedad por propiedad y devuelve true si no hay diferencias
    orig_values = cto_almacenado.__dict__
    for k, v in cto.__dict__.items():
        if orig_values[k] != v:
            return False
    return True

# endregion
