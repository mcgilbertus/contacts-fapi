import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get("/", include_in_schema=False)
def show_docs():
    return RedirectResponse(url="/docs")


app.include_router(contactos_router)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
