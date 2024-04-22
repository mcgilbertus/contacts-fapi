from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from api.model.contacto_modelos import ContactoModel, ContactoSinIdModel
from data.database import db_instance
from data.repositories.contactos_repo import ContactosRepo
from domain.exceptions.NotFound import NotFoundError
from domain.model.contacto import Contacto

contactos_router = APIRouter(prefix='/contactos')
repo = ContactosRepo()


@contactos_router.get('/', response_model=List[ContactoModel], response_model_exclude_none=True)
def get_all(db: Session = Depends(db_instance.get_db)):
    return repo.get_all(db)


@contactos_router.get('/{id}', response_model=ContactoModel)
def get_by_id(id: int, db: Session = Depends(db_instance.get_db)):
    try:
        cto = repo.get_by_id(db, id)
        return cto
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacto no encontrado")


@contactos_router.post('/', response_model=ContactoModel, status_code=status.HTTP_201_CREATED)
def agregar(data: ContactoSinIdModel, db: Session = Depends(db_instance.get_db)):
    contacto = Contacto(**data.model_dump(exclude_unset=True))
    c = repo.agregar(db, contacto)
    return c


@contactos_router.put('/{id}', response_model=ContactoModel)
def editar(id: int, data: ContactoSinIdModel, db: Session = Depends(db_instance.get_db)):
    try:
        c = repo.editar(db, id, data.model_dump(exclude_unset=True))
        return c
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacto no encontrado")


@contactos_router.delete('/{id}', status_code=204, response_class=Response)
def borrar(id: int, db: Session = Depends(db_instance.get_db)):
    try:
        repo.borrar(db, id)
        return
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacto no encontrado")
