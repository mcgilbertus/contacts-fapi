from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from data.database import get_db
from data.repositories.contactos_repo import ContactosRepository
from domain.Contactos import Contacto, ContactoSinId


contactos_router = APIRouter(prefix='/contactos')
repo = ContactosRepository()


@contactos_router.get('/', response_model=List[Contacto])
def get_all(db: Session = Depends(get_db)):
    return repo.get_all(db)


@contactos_router.get('/{id}', response_model=Contacto)
def get_by_id(id: int, db: Session = Depends(get_db)):
    cto = repo.get_by_id(db, id)
    if cto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacto no encontrado")
    return cto


@contactos_router.post('/', response_model=Contacto, status_code=status.HTTP_201_CREATED)
def agregar(data: ContactoSinId, db: Session = Depends(get_db)):
    c = repo.agregar(db, data)
    return c

@contactos_router.put('/{id}', response_model=Contacto)
def editar(id: int, datos: ContactoSinId, db:Session = Depends(get_db)):
    c = repo.actualizar(db, id, datos)
    if c is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacto no encontrado")
    return c


@contactos_router.delete('/{id}', status_code=204, response_class=Response)
def borrar(id: int, db:Session = Depends(get_db)):
    c = repo.borrar(db, id)
    if c is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacto no encontrado")
    return
