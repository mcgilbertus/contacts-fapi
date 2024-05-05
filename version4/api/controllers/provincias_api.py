from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from api.model.provincia_modelos import ProvinciaListModel, ProvinciaUpdateModel, ProvinciaDetailModel
from data.database import db_instance
from data.repositories.provincias_repo import ProvinciasRepo
from domain.exceptions.NotFound import NotFoundError
from domain.model.provincia import Provincia

provincias_router = APIRouter(prefix='/provincias', tags=['Provincias'])
repo = ProvinciasRepo()


@provincias_router.get('/', response_model=List[ProvinciaListModel], response_model_exclude_none=True)
def get_all(db: Session = Depends(db_instance.get_db)):
    return repo.get_all(db)


@provincias_router.get('/{id}', response_model=ProvinciaDetailModel)
def get_by_id(id: int, db: Session = Depends(db_instance.get_db)):
    try:
        cto = repo.get_by_id(db, id)
        return cto
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provincia no encontrada")


@provincias_router.post('/', response_model=ProvinciaDetailModel, status_code=status.HTTP_201_CREATED)
def agregar(data: ProvinciaUpdateModel, db: Session = Depends(db_instance.get_db)):
    provincia = Provincia(**data.model_dump(exclude_unset=True))
    c = repo.agregar(db, provincia)
    return c


@provincias_router.put('/{id}', response_model=ProvinciaDetailModel)
def editar(id: int, data: ProvinciaUpdateModel, db: Session = Depends(db_instance.get_db)):
    try:
        c = repo.editar(db, id, data.model_dump(exclude_unset=True))
        return c
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provincia no encontrada")


@provincias_router.delete('/{id}', status_code=204, response_class=Response)
def borrar(id: int, db: Session = Depends(db_instance.get_db)):
    try:
        repo.borrar(db, id)
        return
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provincia no encontrada")
