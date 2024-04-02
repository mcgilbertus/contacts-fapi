import uvicorn
from fastapi import FastAPI
from data import database

# importamos el modulo para que sqlalchemy tenga registrados los modelos al crear las tablas
from api.contactos_api import contactos_router

database.create_all()

app = FastAPI()

app.include_router(contactos_router)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
