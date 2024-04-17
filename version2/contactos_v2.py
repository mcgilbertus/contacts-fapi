import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from api.controllers.contactos_api import contactos_router

app = FastAPI(
    title='Contactos v2',
    description='Aplicación demo de FastAPI v2',
    version="2.0",
)


# redirección a la documentación por defecto
@app.get("/", include_in_schema=False)
def show_docs():
    return RedirectResponse(url="/docs")


# incluir todas las rutas de contactos
app.include_router(contactos_router)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
