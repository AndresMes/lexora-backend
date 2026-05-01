from fastapi import FastAPI
from .api.routes.invoice_router import invoice_router
import app.models

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(invoice_router)