from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.model.localidad_modelos import LocalidadListModel, LocalidadDetailModel, LocalidadCreateModel, LocalidadUpdateModel, \
    LocalidadResponseModel
from data.database import db_instance
from data.repositories.localidades_repo import LocalidadesRepo
from domain.exceptions.NotFound import NotFoundError
from domain.model.localidad import Localidad

localidades_router = APIRouter(tags=['Localidades'])
repo = LocalidadesRepo()


@localidades_router.get('/localidades', response_model=List[LocalidadListModel], response_model_exclude_none=True)
def get_all(db: Session = Depends(db_instance.get_db)):
    result = repo.get_all(db)
    return result


@localidades_router.get('/localidades/{id}', response_model=LocalidadDetailModel)
def get_by_id(id: int, db: Session = Depends(db_instance.get_db)):
    try:
        cto = repo.get_by_id(db, id)
        return cto
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Localidad no encontrada")


@localidades_router.get('/provincias/{prov_id}/localidades',
                        response_model=List[LocalidadDetailModel],
                        summary='Devuelve todas las localidades de una provincia')
def get_by_prov(prov_id: int, db: Session = Depends(db_instance.get_db)):
    result = repo.get_all_locs_of_prov(db, prov_id)
    return result


@localidades_router.post('/localidades', response_model=LocalidadDetailModel,
                         status_code=status.HTTP_201_CREATED)
def agregar(data: LocalidadCreateModel, db: Session = Depends(db_instance.get_db)):
    try:
        localidad = Localidad(**data.model_dump(exclude_unset=True))
        c = repo.agregar(db, localidad)
        return c
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Error {e.orig.args[0]}: {e.orig.args[1]}")


@localidades_router.put('/localidades/{id}', response_model=LocalidadDetailModel)
def editar(id: int, data: LocalidadUpdateModel, db: Session = Depends(db_instance.get_db)):
    try:
        c = repo.editar(db, id, data.model_dump(exclude_unset=True))
        return c
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Error {e.orig.args[0]}: {e.orig.args[1]}")
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Localidad no encontrada")


@localidades_router.delete('/localidades/{id}', status_code=204, response_class=Response)
def borrar(id: int, db: Session = Depends(db_instance.get_db)):
    try:
        repo.borrar(db, id)
        return
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Localidad no encontrada")
