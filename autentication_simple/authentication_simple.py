import datetime
from typing import List, Annotated

import bcrypt
import uvicorn
from fastapi import FastAPI, HTTPException, Response, status, Header
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field

app = FastAPI(
    title='Contactos con seguridad-v1',
    description='Aplicación demo de FastAPI-seg v1',
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


class User(BaseModel):
    nombre: str
    pwdhash: bytes


# endregion

# region almacenamiento de datos
def hash_password(password: str) -> bytes:
    pwd_bytes = password.encode('utf-8')  # convierte a bytes
    salt = bcrypt.gensalt()  # genera un array de bytes aleatorio llamado 'sal' (salt)
    result = bcrypt.hashpw(pwd_bytes, salt)  # genera el hash de la contraseña+salt
    return result


contactos = [Contacto(id=1, nombre='Contacto1', direccion='dir1', telefonos='tel1', fecha_nac=datetime.date(1999, 8, 23)),
             Contacto(id=2, nombre='Contacto2', direccion='dir2'),
             Contacto(id=3, nombre='Contacto3')]
users = [User(nombre='user1', pwdhash=hash_password('user123')),
         User(nombre='admin', pwdhash=hash_password('admin123')),
         User(nombre='user2', pwdhash=hash_password('user123'))]


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


def buscar_usuario(username: str, pwd: str) -> (User, int):
    i, u = next(((i, u) for i, u in enumerate(users)
                 if u.nombre == username and bcrypt.checkpw(pwd.encode('utf-8'), u.pwdhash)),
                (None, None))
    if u is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autorizado")
    return u, i


# endregion

# region endpoints

## show swagger page to start
@app.get("/", include_in_schema=False)
def show_docs():
    return RedirectResponse(url="/docs")


## GET lista de contactos
## el nombre de usuario y la contraseña en la URL, visibles para todo el mundo
## NO HAGAN ESTO!!
@app.get('/contactos', response_model=List[Contacto], response_model_exclude_none=True)
def get_all(username: str | None = None, pwd: str | None = None):
    """
    Obtiene la lista completa de contactos
    """
    buscar_usuario(username, pwd)
    return contactos


## GET contacto por id
## username y password en headers
## Mejor que el anterior, pero todavia se puede mejorar
@app.get('/contactos/{id}', response_model=Contacto)
def get_contacto(id: int, username: str | None = Header(alias='x-username'), pwd: str | None = Header(alias='x-password')):
    """
    Devuelve la información completa para un Contacto específico
    Espera el nombre de usuario y la contraseña en headers
    """
    buscar_usuario(username, pwd)
    contacto, index = buscar_contacto(id)
    return contacto


## POST crear contacto nuevo
@app.post('/contactos', response_model=Contacto, status_code=201, response_model_exclude_none=True)
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
    uvicorn.run(app, host="127.0.0.1", port=8000, )
