import datetime

import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from data.repositories.contactos_repo import ContactosRepo
from domain.exceptions.NotFound import NotFoundError
from domain.model.contacto import Contacto
from domain.model.direccion import Direccion
from fixtures_data import inicializa_datos_contacto as repo, db_test as db


# region get_all
def test_getAll_devuelveLista(db: Session, datosContacto: ContactosRepo):
    data = datosContacto.get_all(db)
    assert len(data) == 3
    # verifica que se recibieron todos los contactos almacenados, con los mismos valores
    for c in data:
        cto = datosContacto.get_by_id(db, c.id)
        assert c.nombre == cto.nombre
        assert c.telefonos == cto.telefonos
        assert c.fecha_nac == cto.fecha_nac
        assert c.dir == cto.direccion
        if c.localidad is None:
            assert cto.localidad is None
        else:
            assert cto.localidad == c.localidad.nombre


# endregion

# region get_by_id
def test_getById_idCorrecto_devuelveContacto(db: Session, datosContacto: ContactosRepo):
    data = datosContacto.get_by_id(db, 2)
    assert busca_contacto_y_compara(db, data, datosContacto)


def test_getById_idIncorrecto_notFoundError(db: Session, datosContacto: ContactosRepo):
    with pytest.raises(NotFoundError):
        datosContacto.get_by_id(db, 99)


# endregion

# region agregar
def test_agregar_todosLosCampos_devuelveContacto(db: Session, datosContacto: ContactosRepo):
    payload = Contacto(nombre='nuevo contacto', telefonos='1234567890',
                       fecha_nac=datetime.date(2000, 1, 2),
                       direccion=Direccion(calle='nueva direccion', numero=123))
    data = datosContacto.agregar(db, payload)
    assert busca_contacto_y_compara(db, data, datosContacto)


def test_agregar_DirNone_devuelveContacto(db: Session, datosContacto: ContactosRepo):
    payload = Contacto(nombre='nuevo contacto', telefonos='1234567890',
                       fecha_nac=datetime.date(2000, 1, 2),
                       direccion=None)
    data = datosContacto.agregar(db, payload)
    assert busca_contacto_y_compara(db, data, datosContacto)


def test_agregar_soloReq_devuelveContacto(db: Session, datosContacto: ContactosRepo):
    payload = Contacto(nombre='nuevo contacto')
    data = datosContacto.agregar(db, payload)
    assert busca_contacto_y_compara(db, data, datosContacto)


def test_agregar_locInexistente_errorIntegridad(db: Session, datosContacto: ContactosRepo):
    payload = Contacto(nombre='nuevo contacto', telefonos='1234567890',
                       fecha_nac=datetime.date(2000, 1, 2),
                       direccion=Direccion(calle='nueva direccion', numero=123, localidad_id=99))
    with pytest.raises(IntegrityError):
        datosContacto.agregar(db, payload)


# end region

# region editar
def test_editar_todoBien_devuelveContacto(db: Session, datosContacto: ContactosRepo):
    payload = {'nombre': 'nuevo contacto', 'direccion': {'calle': 'nueva direccion', 'numero': 123}}
    data = datosContacto.editar(db, 1, payload)
    assert busca_contacto_y_compara(db, data, datosContacto)


# endregion

# region borrar
def test_borrar_idCorrecto_borraContacto(db: Session, datosContacto: ContactosRepo):
    datosContacto.borrar(db, 1)
    # verifica que el contacto no exista mas en el almacenamiento
    # no se puede usar get_by_id porque el contacto esta en memoria
    assert db.scalar(text('SELECT id FROM Contactos WHERE id = 1')) == None


def test_borrar_idIncorrecto_notFoundError(db: Session, datosContacto: ContactosRepo):
    with pytest.raises(NotFoundError):
        datosContacto.borrar(db, 99)


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
