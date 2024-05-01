import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from data.repositories.localidades_repo import LocalidadesRepo
from domain.exceptions.NotFound import NotFoundError
from domain.model.localidad import Localidad
from fixtures_data import inicializa_datos_localidad as repo, db_test as db


# region get_all
def test_getAll_devuelveLista(db: Session, repoLocalidad: LocalidadesRepo):
    data = repoLocalidad.get_all(db)
    assert len(data) == 3
    # verifica que se recibieron todos los localidades almacenados, con los mismos valores
    for c in data:
        assert busca_localidad_y_compara(db, c, repoLocalidad)


# endregion

# region get_by_id
def test_getById_idCorrecto_devuelveLocalidad(db: Session, repoLocalidad: LocalidadesRepo):
    data = repoLocalidad.get_by_id(db, 2)
    assert busca_localidad_y_compara(db, data, repoLocalidad)


def test_getById_idIncorrecto_notFoundError(db: Session, repoLocalidad: LocalidadesRepo):
    with pytest.raises(NotFoundError):
        repoLocalidad.get_by_id(db, 99)


# endregion

# region agregar
def test_agregar_todoBien_devuelveLocalidad(db: Session, repoLocalidad: LocalidadesRepo):
    payload = Localidad(nombre= 'nuevo localidad', provincia_id= 1)
    data = repoLocalidad.agregar(db, payload)
    assert busca_localidad_y_compara(db, data, repoLocalidad)


# end region

# region editar
def test_editar_todoBien_devuelveLocalidad(db: Session, repoLocalidad: LocalidadesRepo):
    payload = {'nombre': 'nuevo localidad', 'direccion': 'nueva direccion'}
    data = repoLocalidad.editar(db, 1, payload)
    assert busca_localidad_y_compara(db, data, repoLocalidad)


# endregion

# region borrar
def test_borrar_idCorrecto_borraLocalidad(db: Session, repoLocalidad: LocalidadesRepo):
    repoLocalidad.borrar(db, 1)
    # verifica que el localidad no exista mas en el almacenamiento
    # no se puede usar get_by_id porque el localidad esta en memoria
    assert db.scalar(text('SELECT id FROM Localidades WHERE id = 1')) == None


def test_borrar_idIncorrecto_notFoundError(db: Session, repoLocalidad: LocalidadesRepo):
    with pytest.raises(NotFoundError):
        repoLocalidad.borrar(db, 99)


# endregion


# region helper functions

def busca_localidad_y_compara(bd: Session, cto: Localidad, repo: LocalidadesRepo) -> bool:
    # busca el localidad almacenado con el mismo id
    cto_almacenado = repo.get_by_id(bd, cto.id)
    # compara los dos localidades propiedad por propiedad y devuelve true si no hay diferencias
    orig_values = cto_almacenado.__dict__
    for k, v in cto.__dict__.items():
        if orig_values[k] != v:
            return False
    return True

# endregion
