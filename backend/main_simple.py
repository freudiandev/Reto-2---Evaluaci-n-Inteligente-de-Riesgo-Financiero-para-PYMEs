from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="PyMEs Risk Assessment API",
    description="Sistema de evaluación de riesgo financiero para PYMEs",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS para permitir conexiones del frontend
origins = [
    "http://localhost:3000",
    "http://localhost:5173", 
    "https://localhost:3000",
    "https://localhost:5173",
    "*"  # Para deployment en producción
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes para deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint raíz
@app.get("/")
async def root():
    return {
        "message": "PyMEs Risk Assessment API - The Orellana's Boyz",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

# Health check simple
@app.get("/health")
async def simple_health():
    return {
        "status": "healthy",
        "message": "API funcionando correctamente"
    }

# Verificar estado de la API
@app.get("/api/v1/health")
async def health():
    return {
        "status": "healthy",
        "message": "PyMEs Risk Assessment API está funcionando correctamente",
        "version": "1.0.0"
    }

# Obtener lista de empresas
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

# Datos para el dashboard
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

# Obtener lista de aplicaciones
@app.get("/api/v1/applications/")
async def list_applications():
    return {
        "applications": [
            {
                "id": 1,
                "company_name": "TechStart S.A.",
                "amount": 50000,
                "status": "pending",
                "risk_score": 75,
                "created_date": "2024-01-15"
            },
            {
                "id": 2,
                "company_name": "Comercial Los Andes",
                "amount": 25000,
                "status": "approved",
                "risk_score": 85,
                "created_date": "2024-01-10"
            },
            {
                "id": 3,
                "company_name": "Servicios Express",
                "amount": 75000,
                "status": "rejected",
                "risk_score": 45,
                "created_date": "2024-01-08"
            }
        ]
    }

# Análisis de riesgo específico
@app.get("/api/v1/risk-analysis/{application_id}")
async def get_risk_analysis(application_id: int):
    return {
        "application_id": application_id,
        "risk_score": 72,
        "risk_level": "medium",
        "factors": {
            "financial_health": 80,
            "payment_history": 65,
            "market_sentiment": 70,
            "sector_risk": 60
        },
        "recommendation": "Aprobado con condiciones especiales",
        "analysis_date": "2024-01-15T10:30:00Z"
    }

# Simulaciones
@app.get("/api/v1/simulations/{application_id}")
async def get_simulations(application_id: int):
    return {
        "application_id": application_id,
        "scenarios": [
            {
                "name": "Optimista",
                "probability": 0.3,
                "risk_score": 85,
                "recommendation": "Aprobado"
            },
            {
                "name": "Conservador",
                "probability": 0.5,
                "risk_score": 72,
                "recommendation": "Aprobado con condiciones"
            },
            {
                "name": "Pesimista",
                "probability": 0.2,
                "risk_score": 45,
                "recommendation": "Rechazado"
            }
        ]
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
