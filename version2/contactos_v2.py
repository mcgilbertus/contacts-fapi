import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from version2.api.controllers.contactos_api import contactos_router

app = FastAPI(
    title='Contactos v1',
    description='Aplicación demo de FastAPI v1',
    version="1.0",
)

@app.get("/", include_in_schema=False)
def show_docs():
    return RedirectResponse(url="/docs")

app.include_router(contactos_router)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
