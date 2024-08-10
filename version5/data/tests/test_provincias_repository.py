import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from data.repositories.provincias_repo import ProvinciasRepo
from domain.exceptions.NotFound import NotFoundError
from domain.model.provincia import Provincia
from fixtures_data import inicializa_datos_provincia as repo, db_test as db


# region get_all
def test_getAll_devuelveLista(db: Session, datosProvincia: ProvinciasRepo):
    data = datosProvincia.get_all(db)
    assert len(data) == 3
    # verifica que se recibieron todos los provincias almacenados, con los mismos valores
    for c in data:
        assert busca_provincia_y_compara(db, c, datosProvincia)


# endregion

# region get_by_id
def test_getById_idCorrecto_devuelveProvincia(db: Session, datosProvincia: ProvinciasRepo):
    data = datosProvincia.get_by_id(db, 2)
    assert busca_provincia_y_compara(db, data, datosProvincia)


def test_getById_idIncorrecto_notFoundError(db: Session, datosProvincia: ProvinciasRepo):
    with pytest.raises(NotFoundError):
        datosProvincia.get_by_id(db, 99)


# endregion

# region agregar
def test_agregar_todoBien_devuelveProvincia(db: Session, datosProvincia: ProvinciasRepo):
    payload = Provincia(nombre= 'nuevo provincia', pais= 'Pais1')
    data = datosProvincia.agregar(db, payload)
    assert busca_provincia_y_compara(db, data, datosProvincia)


# end region

# region editar
def test_editar_todoBien_devuelveProvincia(db: Session, datosProvincia: ProvinciasRepo):
    payload = {'nombre': 'nuevo provincia', 'direccion': 'nueva direccion'}
    data = datosProvincia.editar(db, 1, payload)
    assert busca_provincia_y_compara(db, data, datosProvincia)


# endregion

# region borrar
def test_borrar_idCorrecto_borraProvincia(db: Session, datosProvincia: ProvinciasRepo):
    datosProvincia.borrar(db, 1)
    # verifica que el provincia no exista mas en el almacenamiento
    # no se puede usar get_by_id porque el provincia esta en memoria
    assert db.scalar(text('SELECT id FROM Provincias WHERE id = 1')) == None


def test_borrar_idIncorrecto_notFoundError(db: Session, datosProvincia: ProvinciasRepo):
    with pytest.raises(NotFoundError):
        datosProvincia.borrar(db, 99)


# endregion


# region helper functions

def busca_provincia_y_compara(bd: Session, prv: Provincia, repo: ProvinciasRepo) -> bool:
    # busca el provincia almacenado con el mismo id
    prv_almacenada = repo.get_by_id(bd, prv.id)
    # compara los dos provincias propiedad por propiedad y devuelve true si no hay diferencias
    orig_values = prv_almacenada.__dict__
    for k, v in prv.__dict__.items():
        if orig_values[k] != v:
            return False
    return True

# endregion
