from typing import List

from fastapi import APIRouter, Response, status

from data.repositories.contactos_repo import ContactosRepo
from domain.model.contactos import Contacto, ContactoSinId

contactos_router = APIRouter(prefix='/contactos')

repo = ContactosRepo()


## GET lista de contactos
@contactos_router.get('/contactos', response_model=List[Contacto], response_model_exclude_none=True)
def get_all():
    return repo.get_all()


## GET contacto por id
@contactos_router.get('/contactos/{id}', response_model=Contacto)
def get_contacto(id: int):
    contacto, index = repo.buscar_contacto(id)
    return contacto


## POST crear contacto nuevo
@contactos_router.post('/contactos', response_model=Contacto, status_code=201)
def agregar(data: ContactoSinId):
    return repo.agregar(data)


## PUT actualizar contacto existente
@contactos_router.put('/contactos/{id}', response_model=Contacto)
def editar(id: int, data: ContactoSinId):
    return repo.editar(id, data)


## DELETE borrar contacto
@contactos_router.delete('/contactos/{id}')
def borrar(id: int):
    repo.borrar(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
