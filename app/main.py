from contextlib import asynccontextmanager
import os
import cloudinary
import easyocr
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.api.routes.auth_router import auth_router
from app.api.routes.party_router import party_router 
from app.api.routes.user_router import user_router
from .api.routes.invoice_router import invoice_router
from app.api.routes.audit_log_router import audit_router
import app.models
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.ocr_reader = easyocr.Reader(['es'], gpu=False)
    
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET")
    )
    
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", #Ruta del frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>OCR AI API</title>

        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Segoe UI', sans-serif;
            }

            body {
                background: linear-gradient(135deg, #0f172a, #1e293b);
                color: white;
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                overflow: hidden;
            }

            .container {
                text-align: center;
                padding: 40px;
                max-width: 900px;
            }

            .badge {
                display: inline-block;
                background: rgba(59, 130, 246, 0.15);
                color: #60a5fa;
                padding: 8px 18px;
                border-radius: 999px;
                font-size: 14px;
                margin-bottom: 25px;
                border: 1px solid rgba(96, 165, 250, 0.3);
            }

            h1 {
                font-size: 4rem;
                margin-bottom: 20px;
                background: linear-gradient(to right, #60a5fa, #a78bfa);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }

            p {
                font-size: 1.2rem;
                color: #cbd5e1;
                line-height: 1.8;
                margin-bottom: 40px;
            }

            .buttons {
                display: flex;
                justify-content: center;
                gap: 20px;
                flex-wrap: wrap;
            }

            .btn {
                text-decoration: none;
                padding: 14px 28px;
                border-radius: 14px;
                font-weight: bold;
                transition: 0.3s ease;
            }

            .primary {
                background: #3b82f6;
                color: white;
                box-shadow: 0 0 20px rgba(59, 130, 246, 0.5);
            }

            .primary:hover {
                transform: translateY(-3px);
                background: #2563eb;
            }

            .secondary {
                border: 1px solid rgba(255,255,255,0.2);
                color: white;
                background: rgba(255,255,255,0.05);
            }

            .secondary:hover {
                background: rgba(255,255,255,0.1);
            }

            .glow {
                position: absolute;
                width: 500px;
                height: 500px;
                background: rgba(59, 130, 246, 0.15);
                filter: blur(120px);
                border-radius: 50%;
                top: -100px;
                right: -100px;
            }

            .glow2 {
                position: absolute;
                width: 400px;
                height: 400px;
                background: rgba(168, 85, 247, 0.12);
                filter: blur(120px);
                border-radius: 50%;
                bottom: -100px;
                left: -100px;
            }
        </style>
    </head>

    <body>

        <div class="glow"></div>
        <div class="glow2"></div>

        <div class="container">
            <div class="badge">
                OCR + Artificial Intelligence API
            </div>

            <h1>Vision AI Backend</h1>

            <p>
                Backend inteligente para procesamiento OCR, extracción de texto,
                análisis documental e integración con modelos de IA.
                Construido con FastAPI y arquitectura moderna.
            </p>

            <div class="buttons">
                <a href="/docs" class="btn primary">
                    Open API Docs
                </a>

                <a href="/redoc" class="btn secondary">
                    ReDoc
                </a>
            </div>
        </div>

    </body>
    </html>
    """

app.include_router(invoice_router)
app.include_router(user_router)
app.include_router(party_router)
app.include_router(audit_router)
app.include_router(auth_router)