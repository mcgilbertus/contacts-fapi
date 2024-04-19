import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

# importamos el modulo para que sqlalchemy tenga registrados los modelos al crear las tablas
from api.controllers.contactos_api import contactos_router
from data import database

# crea la instancia de Database para trabajar con la bd 'normal' (no de testing)
database.create_db_prod()
# crear todas las tablas que no existan ya
database.db_instance.create_all()

app = FastAPI()


@app.get("/", include_in_schema=False)
def show_docs():
    return RedirectResponse(url="/docs")


app.include_router(contactos_router)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
