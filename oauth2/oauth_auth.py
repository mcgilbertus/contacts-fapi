import datetime
import hashlib
import json
import logging
import uuid
from datetime import timezone
from logging import getLogger
from typing import Annotated, List

import bcrypt
import requests
from fastapi import FastAPI, HTTPException, Response, status, Form, Request, Header, Query
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from jose import jws
from jose.utils import base64url_encode
from pydantic import BaseModel, Field

logger = getLogger(__name__)

app = FastAPI(
    title='Contactos con seguridad-OAuth2',
    description='Aplicación demo de FastAPI-OAuth2',
    version="2.1",
    swagger_ui_init_oauth={
        "appName": "Contacts API",
        "clientId": "m2m",
        "scopes": "api"
    },
)
templates = Jinja2Templates(directory="templates")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# oauth2_scheme = OAuth2AuthorizationCodeBearer(
#     authorizationUrl="https://demo.duendesoftware.com/connect/authorize",
#     tokenUrl="https://demo.duendesoftware.com/connect/token")

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

auth_server = "https://localhost:5001"  # se puede tomar de una variable de entorno o de un archivo de configuración
# auth_server = "https://demo.duendesoftware.com"
discovery_url = f"{auth_server}/.well-known/openid-configuration"
audience = 'api1'
issuer = auth_server
cl_id_pwd = 'client_pwd'
cl_id_code = 'client_code'
cl_id_pkce = 'client_pkce'
cl_secret = 'secret'
scope = 'api1.access openid profile'
code_verifier = base64url_encode(b"This_is_a_text_long_enough_to_be_used_as_a_code_verifier")


# region token helpers

def get_token_from_auth_header(token_header: str) -> str:
    """
    Extrae el token Bearer del header de autorización
    """
    try:
        scheme, _, token = token_header.partition(" ")
        if scheme.lower() == 'bearer':
            return token
    except Exception as e:
        logger.error(f"Error al procesar el header Authorization: {e}")

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autorizado")


def nueva_sesion():
    return str(uuid.uuid4())


def verifica_token(token: str) -> dict:
    """
    Verifica el token recibido y, si es valido, devuelve el payload
    """
    try:
        if token is None:
            raise Exception("No se recibió el token")

        header = jws.get_unverified_header(token)
        sign_key = get_public_key(header['kid'])
        payload = json.loads(jws.verify(token, sign_key, algorithms=header['alg'], verify=True))
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


discovery_doc_cache = None


def get_discovery():
    """
    Obtiene la configuración del servidor de autenticación.
    La guarda en cache para no tener que pedirla cada vez
    """
    global discovery_doc_cache

    if discovery_doc_cache is None:
        try:
            response = requests.get(discovery_url, verify=False)
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=response.text)
            discovery_doc_cache = response.json()
        except Exception as e:
            logger.error(f"Error al obtener la configuración del servidor de autenticación: {e}")
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                detail="No se pudo obtener la configuración del servidor de autenticación")

    return discovery_doc_cache


def get_public_key(kid: str):
    """
    Obtiene la clave pública para verificar la firma del token
    """
    discovery_doc = get_discovery()
    keyset_url = discovery_doc['jwks_uri']
    jwks = requests.get(keyset_url, verify=False).json()
    key = next((k for k in jwks['keys'] if k['kid'] == kid), None)
    return key


# endregion


## show swagger page to start
@app.get("/", include_in_schema=False)
def show_docs():
    return RedirectResponse(url="/docs")


# region discovery doc
@app.get("/discovery")
def get_discovery_doc():
    return get_discovery()


# endregion


# region client credentials flow
@app.get("/client-creds")
def get_client_token(client_id: str, client_secret: str, scope: str):
    discovery_doc = get_discovery()
    response = requests.post(discovery_doc['token_endpoint'],
                             data={
                                 'grant_type': 'client_credentials',
                                 'client_id': client_id,
                                 'client_secret': client_secret,
                                 'scope': scope
                             }, verify=False)
    if response.status_code != 200:
        logger.error(f"Error {response.status_code} al autenticar cliente: {response.text}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autorizado")

    auth = response.json()
    return auth


# endregion


# region password flow
# login page
@app.get("/login-local")
def login_page(req: Request, nexturl: str = Query(default=None)):
    return templates.TemplateResponse('login.html', {'request': req, 'nexturl': nexturl})


# Verifica el usuario, contraseña y client_id y devuelve un token JWT. Llamado desde
# el formulario de login de /login-local
@app.post('/gettoken')
def get_token(username: str = Form(), password: str = Form()):
    discovery_doc = get_discovery()
    response = requests.post(discovery_doc['token_endpoint'],
                             data={
                                 'grant_type': 'password',
                                 'client_id': cl_id_pwd,
                                 'client_secret': cl_secret,
                                 'username': username,
                                 'password': password,
                                 'scope': scope
                             }, verify=False)
    if response.status_code != 200:
        logger.error(f"Error {response.status_code} al autenticar usuario: {response.text}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autorizado")

    auth = response.json()
    return auth


# endregion


# region code flow
@app.get("/login-code")
def login_code(req: Request, nexturl: str = Query(default=None)):
    discovery_doc = get_discovery()
    Response = RedirectResponse(f"{discovery_doc['authorization_endpoint']}?"
                                f"response_type=code&"
                                f"client_id={cl_id_code}&"
                                f"scope={scope}&"
                                f"redirect_uri=http://localhost:8000/code-callback")
    return Response


@app.get("/code-callback")
def code_callback(code: str):
    discovery_doc = get_discovery()
    response = requests.post(discovery_doc['token_endpoint'],
                             data={
                                 'grant_type': 'authorization_code',
                                 'code': code,
                                 'client_id': cl_id_code,
                                 'client_secret': cl_secret,
                                 'redirect_uri': 'http://localhost:8000/code-callback'
                             }, verify=False)
    if response.status_code != 200:
        logger.error(f"Error {response.status_code} al autenticar usuario: {response.text}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autorizado")

    auth = response.json()
    return auth


# endregion


# region code with PKCE flow
@app.get("/pkce-callback")
def pkce_callback(req: Request, code: str):
    session_state = base64url_encode("some state value".encode('utf-8')).decode('utf-8')
    if session_state != req.query_params['state']:
        logger.debug("El estado no coincide")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autorizado")

    discovery_doc = get_discovery()
    response = requests.post(discovery_doc['token_endpoint'],
                             data={
                                 'grant_type': 'authorization_code',
                                 'code': code,
                                 'client_id': cl_id_pkce,
                                 'client_secret': cl_secret,
                                 'code_verifier': code_verifier.decode('utf-8'),
                                 'redirect_uri': 'http://localhost:8000/pkce-callback'
                             }, verify=False)
    if response.status_code != 200:
        logger.error(f"Error {response.status_code} al autenticar usuario: {response.text}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autorizado")

    auth = response.json()
    return auth


# login with code and PKCE flow
@app.get("/login-pkce")
def login_pkce(req: Request, nexturl: str = Query(default=None)):
    discovery_doc = get_discovery()
    session_state = base64url_encode("some state value".encode('utf-8')).decode('utf-8')
    code_challenge = base64url_encode(hashlib.sha256(code_verifier).digest()).decode('utf-8')
    Response = RedirectResponse(f"{discovery_doc['authorization_endpoint']}?"
                                f"response_type=code&"
                                f"client_id={cl_id_pkce}&"
                                f"scope={scope}&"
                                f"state={session_state}&"
                                # f"nonce={nonce}&"
                                f"code_challenge={code_challenge}&"
                                f"code_challenge_method=S256&"
                                f"redirect_uri=http://localhost:8000/pkce-callback")
    return Response


# endregion


# region endpoints
## GET lista de contactos
@app.get('/contactos', response_model=List[Contacto], response_model_exclude_none=True)
def get_all(auth_header: str = Header(alias='Authorization', default=None)):
    token = get_token_from_auth_header(auth_header)  # verifica que el header empiece con 'Bearer' y devuelve el token
    claims = verifica_token(token)  # verifica el token y devuelve el diccionario de claims
    logger.info(f'Token claims: {claims}')
    logger.info(f'Usuario autenticado')
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

    logger.level = logging.INFO
    logger.handlers = [logging.StreamHandler()]
    uvicorn.run(app, host="127.0.0.1", port=8000, )
