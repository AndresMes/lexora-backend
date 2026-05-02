from fastapi import FastAPI

from app.api.routes.user_router import user_router
from .api.routes.invoice_router import invoice_router
import app.models

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(invoice_router)
app.include_router(user_router)