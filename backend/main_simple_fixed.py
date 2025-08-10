"""
Backend ultra-simple para deployment inmediato en Render
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os

# FastAPI app
app = FastAPI(
    title="PyMEs Risk Assessment API",
    description="Sistema de evaluación de riesgo para PYMEs - The Orellana's Boyz",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "PyMEs AI Risk Assessment System - The Orellana's Boyz",
        "version": "2.0.0",
        "status": "operational",
        "features": ["Dashboard Analytics", "Risk Assessment", "Company Management"],
        "docs": "/docs",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "system_status": "operational",
        "database_status": "ready",
        "ai_status": "active",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/v1/dashboard/summary")
async def dashboard_summary():
    """Dashboard con datos para el hackathon"""
    return {
        "total_applications": 48,
        "approved_applications": 32,
        "rejected_applications": 10,
        "pending_applications": 6,
        "average_risk_score": 72.3,
        "total_credit_amount": 2750000,
        "risk_level_distribution": {
            "low": 18,
            "medium": 22,
            "high": 8
        },
        "sector_distribution": {
            "Tecnología": 12,
            "Comercio": 15,
            "Manufactura": 10,
            "Servicios": 11
        },
        "ai_insights": {
            "model_accuracy": 0.89,
            "predictions_today": 24,
            "companies_analyzed": 48,
            "sentiment_analysis_coverage": 0.75
        }
    }

@app.get("/api/v1/companies/")
async def get_companies():
    """Lista de empresas de ejemplo"""
    return {
        "companies": [
            {
                "id": 1,
                "name": "TechStart Ecuador S.A.",
                "ruc": "1234567890001",
                "sector": "Tecnología",
                "risk_score": 85
            },
            {
                "id": 2,
                "name": "Comercial Los Andes Cía. Ltda.",
                "ruc": "0987654321001",
                "sector": "Comercio",
                "risk_score": 72
            },
            {
                "id": 3,
                "name": "Manufactura Moderna S.A.",
                "ruc": "1122334455001",
                "sector": "Manufactura",
                "risk_score": 68
            },
            {
                "id": 4,
                "name": "Servicios Express Quito",
                "ruc": "5566778899001",
                "sector": "Servicios",
                "risk_score": 79
            },
            {
                "id": 5,
                "name": "Consultoría Integral S.A.",
                "ruc": "9988776655001",
                "sector": "Servicios",
                "risk_score": 81
            }
        ]
    }

@app.get("/api/v1/applications/")
async def get_applications():
    """Lista de aplicaciones de crédito"""
    return {
        "applications": [
            {
                "id": 1,
                "company_name": "TechStart Ecuador S.A.",
                "amount": 75000,
                "status": "approved",
                "risk_score": 85,
                "created_date": "2024-01-15"
            },
            {
                "id": 2,
                "company_name": "Comercial Los Andes",
                "amount": 50000,
                "status": "pending",
                "risk_score": 72,
                "created_date": "2024-01-14"
            },
            {
                "id": 3,
                "company_name": "Manufactura Moderna",
                "amount": 100000,
                "status": "under_review",
                "risk_score": 68,
                "created_date": "2024-01-13"
            },
            {
                "id": 4,
                "company_name": "Servicios Express",
                "amount": 30000,
                "status": "approved",
                "risk_score": 79,
                "created_date": "2024-01-12"
            },
            {
                "id": 5,
                "company_name": "Consultoría Integral",
                "amount": 45000,
                "status": "rejected",
                "risk_score": 45,
                "created_date": "2024-01-11"
            }
        ]
    }

@app.get("/api/v1/risk-analysis/{application_id}")
async def get_risk_analysis(application_id: int):
    """Análisis de riesgo detallado"""
    
    # Datos simulados basados en ID
    base_score = 60 + (application_id % 30)
    
    return {
        "application_id": application_id,
        "risk_score": base_score,
        "risk_level": "medium" if 50 <= base_score <= 75 else ("low" if base_score > 75 else "high"),
        "factors": {
            "financial_health": base_score * 0.4,
            "payment_history": (base_score + 5) * 0.3,
            "market_sentiment": (base_score - 3) * 0.2,
            "sector_risk": (base_score + 2) * 0.1
        },
        "recommendation": f"Score: {base_score}/100 - " + ("Aprobado" if base_score > 70 else "Evaluación adicional"),
        "analysis_date": datetime.now().isoformat(),
        "ai_confidence": 0.87
    }

@app.get("/api/v1/simulations/{application_id}")
async def get_simulations(application_id: int):
    """Simulaciones de escenarios"""
    
    base_score = 65 + (application_id % 25)
    
    return {
        "application_id": application_id,
        "scenarios": [
            {
                "name": "Optimista",
                "probability": 0.25,
                "risk_score": min(100, base_score + 20),
                "recommendation": "Aprobado con condiciones favorables"
            },
            {
                "name": "Conservador",
                "probability": 0.55,
                "risk_score": base_score,
                "recommendation": "Aprobado con condiciones estándar"
            },
            {
                "name": "Pesimista",
                "probability": 0.20,
                "risk_score": max(20, base_score - 25),
                "recommendation": "Requiere garantías adicionales"
            }
        ],
        "generated_at": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    print(f"""
🚀 PyMEs Risk Assessment System - ULTRA SIMPLE
📍 URL: http://{host}:{port}
📖 Docs: http://{host}:{port}/docs
🎯 Ready for Hackathon Demo!
    """)
    
    uvicorn.run(app, host=host, port=port)
