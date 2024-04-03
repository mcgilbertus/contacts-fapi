import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from data import database

# importamos el modulo para que sqlalchemy tenga registrados los modelos al crear las tablas
from api.controllers.contactos_api import contactos_router

# crear todas las tablas que no existan ya
# database.create_all()
# reemplazado por Alembic para implementar migraciones

app = FastAPI()


@app.get("/", include_in_schema=False)
def show_docs():
    return RedirectResponse(url="/docs")


app.include_router(contactos_router)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
