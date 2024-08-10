import datetime
import json
import uuid
from datetime import timezone
from logging import getLogger
from typing import Annotated, List

import bcrypt
from fastapi import FastAPI, HTTPException, Response, status, Form, Header, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from jose import jws
from pydantic import BaseModel, Field

logger = getLogger(__name__)

app = FastAPI(
    title='Contactos con seguridad-JWT',
    description='Aplicación demo de FastAPI-seg v2',
    version="2.0",
)
app.mount("/static", StaticFiles(directory="static"), name="static")


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

super_secret_key = 'secret'
audience = 'api.contacts'
issuer = 'contacts-fapi'

# token helpers
def nueva_sesion():
    return str(uuid.uuid4())

def create_session_token(username: str) -> str:
    claims = {
        'iss': 'contacts-fapi',
        'sub': username,
        'session': nueva_sesion(),
        'aud': 'api.contacts',
        'exp': int((datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(minutes=30)).timestamp())
    }
    signed = jws.sign(claims, super_secret_key, algorithm='HS256')
    return signed


def verifica_token(auth_header: str) -> dict:
    try:
        if auth_header is None:
            raise Exception("No se recibió el token")
        if not auth_header.startswith("Bearer "):
            raise Exception("El token debe empezar con 'Bearer '")

        access_token = auth_header.split(' ')[1]

        payload = json.loads(jws.verify(access_token, super_secret_key, algorithms=['HS256']))
        if payload['exp'] < datetime.datetime.now(tz=timezone.utc).timestamp():
            raise Exception("Token expirado")
        if payload['aud'] != audience:
            raise Exception("Token no válido para este servicio")
        if payload['iss'] != issuer:
            raise Exception("El emisor no es válido")

        logger.info('Token verificado correctamente')
        return payload
    except Exception as e:
        logger.error("Error al verificar token:")
        logger.error(f"  {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autorizado")


# region endpoints

## show swagger page to start
@app.get("/", include_in_schema=False)
def show_docs():
    return RedirectResponse(url="/docs")


# login page
@app.get("/login")
def login_page():
    return HTMLResponse(content=open('static/login.html').read(), status_code=200)


# Verifica el usuario y contraseña y devuelve un token JWT
@app.post('/login')
def login(username: str = Form(), pwd: str = Form()):
    u, i = buscar_usuario(username, pwd)
    return {'access_token': create_session_token(username), 'token_type': 'Bearer'}


## GET lista de contactos
@app.get('/contactos', response_model=List[Contacto], response_model_exclude_none=True)
def get_all(req: Request, auth_header: str = Header(alias='Authorization', default=None)):
    claims = verifica_token(auth_header)
    logger.info(f'Usuario autenticado: {claims["sub"]}, sesion: {claims["session"]}')
    return contactos


## GET contacto por id
@app.get('/contactos/{id}', response_model=Contacto)
def get_contacto(id: int):
    """
    Devuelve la información completa para un Contacto específico
    Espera el nombre de usuario y la contraseña en headers
    """
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
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, )
