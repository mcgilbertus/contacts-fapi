import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from data.repositories.localidades_repo import LocalidadesRepo
from domain.exceptions.NotFound import NotFoundError
from domain.model.localidad import Localidad
from fixtures_data import inicializa_datos_localidad as repo, db_test as db


# region get_all
def test_getAll_devuelveLista(db: Session, datosLocalidad: LocalidadesRepo):
    data = datosLocalidad.get_all(db)
    assert len(data) == 3
    # verifica que se recibieron todos los localidades almacenados, con los mismos valores
    for c in data:
        cto_almacenado = datosLocalidad.get_by_id(db, c.id)
        assert c.nombre == cto_almacenado.nombre
        if c.provincia is None:
            assert cto_almacenado.provincia == None
        else:
            assert c.provincia == cto_almacenado.provincia.nombre



# endregion

# region get_by_id
def test_getById_idCorrecto_devuelveLocalidad(db: Session, datosLocalidad: LocalidadesRepo):
    data = datosLocalidad.get_by_id(db, 2)
    assert busca_localidad_y_compara(db, data, datosLocalidad)


def test_getById_idIncorrecto_notFoundError(db: Session, datosLocalidad: LocalidadesRepo):
    with pytest.raises(NotFoundError):
        datosLocalidad.get_by_id(db, 99)


# endregion

#region agregar

def test_agregar_todoBien_devuelveLocalidad(db: Session, datosLocalidad: LocalidadesRepo):
    payload = Localidad(nombre= 'nuevo localidad', provincia_id= 1)
    data = datosLocalidad.agregar(db, payload)
    assert busca_localidad_y_compara(db, data, datosLocalidad)

#endregion

# region editar
def test_editar_todoBien_devuelveLocalidad(db: Session, datosLocalidad: LocalidadesRepo):
    payload = {'nombre': 'nuevo localidad', 'direccion': 'nueva direccion'}
    data = datosLocalidad.editar(db, 1, payload)
    assert busca_localidad_y_compara(db, data, datosLocalidad)


# endregion

# region borrar
def test_borrar_idCorrecto_borraLocalidad(db: Session, datosLocalidad: LocalidadesRepo):
    datosLocalidad.borrar(db, 1)
    # verifica que el localidad no exista mas en el almacenamiento
    # no se puede usar get_by_id porque el localidad esta en memoria
    assert db.scalar(text('SELECT id FROM Localidades WHERE id = 1')) == None


def test_borrar_idIncorrecto_notFoundError(db: Session, datosLocalidad: LocalidadesRepo):
    with pytest.raises(NotFoundError):
        datosLocalidad.borrar(db, 99)


# endregion


# region helper functions

def busca_localidad_y_compara(bd: Session, loc: Localidad, repo: LocalidadesRepo) -> bool:
    # busca el localidad almacenado con el mismo id
    loc_almacenada = repo.get_by_id(bd, loc.id)
    # compara los dos localidades propiedad por propiedad y devuelve true si no hay diferencias
    orig_values = loc_almacenada.__dict__
    for k, v in loc.__dict__.items():
        if orig_values[k] != v:
            return False
    return True

# endregion
