from fastapi import FastAPI

from app.api.routes.party_router import party_router 
from app.api.routes.user_router import user_router
from .api.routes.invoice_router import invoice_router
from app.api.routes.audit_log_router import audit_router
import app.models

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(invoice_router)
app.include_router(user_router)
app.include_router(party_router)
app.include_router(audit_router)