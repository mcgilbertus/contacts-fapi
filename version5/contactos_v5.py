import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from api.v1.controllers.contactos_api_v1 import contactos_router_v1
from api.v1.controllers.localidades_api import localidades_router
from api.v1.controllers.logging_api import logging_router
from api.v1.controllers.provincias_api import provincias_router
from api.v2.controllers.contactos_api_v2 import contactos_router_v2
from config import Config
from data.database import connect_to_prod

settings = Config('dev', base_file='C:\\archi\\ernesto\\prog\\python\\contacts-fapi\\version5\\settings.json', env_prefix='ENV_').settings
logsettings = settings.get('logging', {})
logging.config.dictConfig(logsettings)

connect_to_prod()

app = FastAPI()


@app.get("/", include_in_schema=False)
def show_docs():
    return RedirectResponse(url="/docs")


app.include_router(logging_router)
app.include_router(contactos_router_v1, prefix='/v1')
app.include_router(contactos_router_v2, prefix='/v2')
app.include_router(contactos_router_v2) # default version
app.include_router(localidades_router)
app.include_router(provincias_router)

# contactos_v5.py

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
