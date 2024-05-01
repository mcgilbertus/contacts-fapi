import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

# importamos el modulo para que sqlalchemy tenga registrados los modelos al crear las tablas
from api.controllers.contactos_api import contactos_router
from api.controllers.localidades_api import localidades_router
from api.controllers.provincias_api import provincias_router
from data.database import db_instance

# crear todas las tablas que no existan ya
db_instance.create_all()

app = FastAPI()


@app.get("/", include_in_schema=False)
def show_docs():
    return RedirectResponse(url="/docs")


app.include_router(contactos_router)
app.include_router(localidades_router)
app.include_router(provincias_router)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
