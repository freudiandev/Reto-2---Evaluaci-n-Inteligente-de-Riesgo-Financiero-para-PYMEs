from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Crear la aplicación FastAPI
app = FastAPI(
    title="PyMEs Risk Assessment API",
    description="Sistema de evaluación de riesgo financiero para PYMEs",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta de salud
@app.get("/api/v1/health")
async def health():
    return {
        "status": "healthy",
        "message": "PyMEs Risk Assessment API está funcionando correctamente",
        "version": "1.0.0"
    }

# Ruta de prueba para empresas
@app.get("/api/v1/companies/")
async def list_companies():
    return {
        "companies": [
            {
                "id": 1,
                "name": "Empresa Demo 1",
                "ruc": "1234567890001",
                "sector": "Tecnología",
                "risk_score": 75
            },
            {
                "id": 2,
                "name": "Empresa Demo 2", 
                "ruc": "0987654321001",
                "sector": "Comercio",
                "risk_score": 60
            }
        ]
    }

# Ruta de prueba para dashboard
@app.get("/api/v1/dashboard/summary")
async def dashboard_summary():
    return {
        "total_companies": 25,
        "total_applications": 48,
        "approved_applications": 32,
        "rejected_applications": 16,
        "average_risk_score": 68.5,
        "risk_distribution": {
            "low": 15,
            "medium": 20, 
            "high": 13
        },
        "sector_distribution": {
            "Tecnología": 8,
            "Comercio": 12,
            "Manufactura": 15,
            "Servicios": 13
        }
    }

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("PORT", os.getenv("API_PORT", 8000)))
    
    print(f"""
🚀 Iniciando PyMEs Risk Assessment API...
📍 URL: http://{host}:{port}
📖 Documentación: http://{host}:{port}/docs
🏥 Health Check: http://{host}:{port}/api/v1/health
    """)
    
    uvicorn.run(app, host=host, port=port)
