from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.model.contacto_modelos import ContactoDetailModel, ContactoUpdateModel, ContactoCreateModel, ContactoListModel
from data.database import db_instance
from data.repositories.contactos_repo import ContactosRepo
from domain.exceptions.NotFound import NotFoundError
from domain.model.contacto import Contacto
from domain.model.direccion import Direccion

contactos_router = APIRouter(prefix='/contactos', tags=['Contactos'])
repo = ContactosRepo()


@contactos_router.get('/', response_model=List[ContactoListModel], response_model_exclude_none=True)
def get_all(db: Session = Depends(db_instance.get_db)):
    return repo.get_all(db)


@contactos_router.get('/{id}', response_model=ContactoDetailModel)
def get_by_id(id: int, db: Session = Depends(db_instance.get_db)):
    try:
        cto = repo.get_by_id(db, id)
        return cto
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacto no encontrado")


@contactos_router.post('/', response_model=ContactoDetailModel, status_code=status.HTTP_201_CREATED)
def agregar(data: ContactoCreateModel, db: Session = Depends(db_instance.get_db)):
    try:
        props = data.model_dump()
        direccion = Direccion(**props.pop('direccion', {}))
        props['direccion'] = direccion
        contacto = Contacto(**props)
        c = repo.agregar(db, contacto)
        return c
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Error {e.orig.args[0]}: {e.orig.args[1]}")


@contactos_router.put('/{id}', response_model=ContactoDetailModel)
def editar(id: int, data: ContactoUpdateModel, db: Session = Depends(db_instance.get_db)):
    try:
        c = repo.editar(db, id, data.model_dump())
        return c
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Error {e.orig.args[0]}: {e.orig.args[1]}")
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacto no encontrado")


@contactos_router.delete('/{id}', status_code=204, response_class=Response)
def borrar(id: int, db: Session = Depends(db_instance.get_db)):
    try:
        repo.borrar(db, id)
        return
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacto no encontrado")
