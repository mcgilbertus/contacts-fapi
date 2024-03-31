import datetime
from typing import List, Annotated
import uvicorn
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field

app = FastAPI(
    title='Contactos v1',
    description='Aplicación demo de FastAPI v1',
    version="1.0",
)


# region modelo
# propiedades comunes, sin id - para Create, Update

class ContactoSinId(BaseModel):
    nombre: Annotated[str, Field(..., description='Nombre y apellido del contacto', max_length=80)]
    direccion: Annotated[str, Field(description='Direccion completa (calle, nro, piso, depto, ciudad, etc)', max_length=120)] = None
    telefonos: Annotated[str, Field(description='Todos los números de teléfono del contacto', max_length=50)] = None
    fecha_nac: Annotated[datetime.date, Field(description='Fecha de nacimiento')] = None


# modelo completo: todo lo de la base mas el id. Para GET y almacenamiento
class Contacto(ContactoSinId):
    id: Annotated[int, Field(gt=0, default_factory=lambda: get_next_id())]


# endregion

# region almacenamiento de datos
contactos = [Contacto(id=1, nombre='Contacto1', direccion='dir1', telefonos='tel1', fecha_nac=datetime.date(1999, 8, 23)),
             Contacto(id=2, nombre='Contacto2', direccion='dir2'),
             Contacto(id=3, nombre='Contacto3')]


def buscar_contacto(id):
    i, c = next(((i, c) for i, c in enumerate(contactos) if c.id == id), (None, None))
    if c is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacto no encontrado")
    return c, i


def get_next_id():
    new_id = 1
    for c in contactos:
        if c.id >= new_id:
            new_id = c.id + 1
    return new_id


# endregion

# region endpoints

## show swagger page to start
@app.get("/", include_in_schema=False)
def show_docs():
    return RedirectResponse(url="/docs")


## GET lista de contactos
@app.get('/contactos', response_model=List[Contacto], response_model_exclude_none=True)
def get_all():
    """
    Obtiene la lista completa de contactos
    """
    return contactos


## GET contacto por id
@app.get('/contactos/{id}', response_model=Contacto)
def get_contacto(id: int):
    """
    Devuelve la información completa para un Contacto específico
    """
    contacto, index = buscar_contacto(id)
    return contacto


## POST crear contacto nuevo
@app.post('/contactos', response_model=Contacto, status_code=201)
def agregar(data: ContactoSinId):
    """
    Agrega un Contacto
    """
    c = Contacto(**data.model_dump(exclude_none=True))
    contactos.append(c)
    return c


## PUT actualizar contacto existente
@app.put('/contactos/{id}', response_model=Contacto)
def editar(id: int, data: ContactoSinId):
    """
    Actualizar datos de un Contacto existente
    """
    c, i = buscar_contacto(id)
    c = c.model_copy(update=data.model_dump(exclude_unset=True))
    contactos[i] = c
    return c


## DELETE borrar contacto
@app.delete('/contactos/{id}')
def borrar(id: int):
    """
    Borrar un Contacto existente
    """
    c, i = buscar_contacto(id)
    contactos.remove(c)
    # segun la especificacion, al borrar un elemento hay que devolver 204 y ningun dato
    # la forma de devolver sólo el código de error es devolver una instancia de Response vacía
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# endregion


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
