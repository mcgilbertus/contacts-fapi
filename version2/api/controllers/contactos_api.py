from typing import List

from fastapi import APIRouter, Response, status, HTTPException

from data.repositories.contactos_repo import ContactosRepo
from domain.exceptions.NotFound import NotFoundError
from domain.model.contactos import Contacto, ContactoSinId

contactos_router = APIRouter(prefix='/contactos', tags=['Contactos'])

repo = ContactosRepo()


## GET lista de contactos
@contactos_router.get('/', response_model=List[Contacto], response_model_exclude_none=True)
def get_all():
    return repo.get_all()


## GET contacto por id
@contactos_router.get('/{id}', response_model=Contacto)
def get_contacto(id: int):
    try:
        contacto, index = repo.buscar_contacto(id)
        return contacto
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")


## POST crear contacto nuevo
@contactos_router.post('/', response_model=Contacto, status_code=201)
def agregar(data: ContactoSinId):
    return repo.agregar(data)


## PUT actualizar contacto existente
@contactos_router.put('/{id}', response_model=Contacto)
def editar(id: int, data: ContactoSinId):
    try:
        return repo.editar(id, data)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")


## DELETE borrar contacto
@contactos_router.delete('/{id}')
def borrar(id: int):
    try:
        repo.borrar(id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")
