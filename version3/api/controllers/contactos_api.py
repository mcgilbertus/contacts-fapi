from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from data.database import db_instance
from data.repositories.contactos_repo import ContactosRepo
from domain.Contactos import Contacto, ContactoSinId
from domain.exceptions.NotFound import NotFoundError

contactos_router = APIRouter(prefix='/contactos')
repo = ContactosRepo()


@contactos_router.get('/', response_model=List[Contacto], response_model_exclude_none=True)
def get_all(db: Session = Depends(db_instance.get_db)):
    return repo.get_all(db)


@contactos_router.get('/{id}', response_model=Contacto)
def get_by_id(id: int, db: Session = Depends(db_instance.get_db)):
    try:
        cto = repo.get_by_id(db, id)
        return cto
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacto no encontrado")


@contactos_router.post('/', response_model=Contacto, status_code=status.HTTP_201_CREATED)
def agregar(data: ContactoSinId, db: Session = Depends(db_instance.get_db)):
    c = repo.agregar(db, data)
    return c


@contactos_router.put('/{id}', response_model=Contacto)
def editar(id: int, datos: ContactoSinId, db: Session = Depends(db_instance.get_db)):
    try:
        c = repo.actualizar(db, id, datos)
        return c
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacto no encontrado")


@contactos_router.delete('/{id}', status_code=204, response_class=Response)
def borrar(id: int, db: Session = Depends(db_instance.get_db)):
    try:
        c = repo.borrar(db, id)
        return
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacto no encontrado")
