from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from app.api.routes import router
from app.services.database import init_db
import os

# Crear la aplicación FastAPI
app = FastAPI(
    title="Evaluación Inteligente de Riesgo Financiero para PYMEs",
    description="API para evaluación de riesgo crediticio usando IA y datos no tradicionales",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Incluir rutas de la API
app.include_router(router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    """Inicializar base de datos al iniciar la aplicación"""
    init_db()

@app.get("/")
async def root():
    return {
        "message": "API de Evaluación Inteligente de Riesgo Financiero para PYMEs",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API funcionando correctamente"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
