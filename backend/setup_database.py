"""
Script para poblar la base de datos con datos de ejemplo
para demostración del sistema de evaluación de riesgo
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main_ai_complete import SessionLocal, Company, FinancialData, engine, Base
from datetime import datetime, timedelta
import random

def create_sample_data():
    """Crear datos de ejemplo para el hackathon"""
    
    # Crear tablas si no existen
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Verificar si ya hay datos
        existing_companies = db.query(Company).count()
        if existing_companies > 0:
            print("✅ Ya existen datos en la base de datos")
            return
        
        print("🔄 Creando datos de ejemplo...")
        
        # Empresas de ejemplo
        companies_data = [
            {
                "ruc": "1234567890001",
                "name": "TechStart Ecuador S.A.",
                "sector": "Tecnología",
                "website": "https://techstart.ec",
                "social_media_presence": 0.8
            },
            {
                "ruc": "0987654321001", 
                "name": "Comercial Los Andes Cía. Ltda.",
                "sector": "Comercio",
                "website": "https://losandes.com.ec",
                "social_media_presence": 0.6
            },
            {
                "ruc": "1122334455001",
                "name": "Manufactura Moderna S.A.",
                "sector": "Manufactura", 
                "website": "https://manufactura.ec",
                "social_media_presence": 0.4
            },
            {
                "ruc": "5566778899001",
                "name": "Servicios Express Quito",
                "sector": "Servicios",
                "website": "https://serviciosexpressqto.ec",
                "social_media_presence": 0.7
            },
            {
                "ruc": "9988776655001",
                "name": "Consultoría Integral S.A.",
                "sector": "Servicios",
                "website": "https://consultoria.ec",
                "social_media_presence": 0.9
            }
        ]
        
        # Crear empresas
        created_companies = []
        for company_data in companies_data:
            company = Company(
                ruc=company_data["ruc"],
                name=company_data["name"],
                sector=company_data["sector"],
                website=company_data["website"],
                social_media_presence=company_data["social_media_presence"],
                foundation_date=datetime.now() - timedelta(days=random.randint(365, 3650))
            )
            db.add(company)
            created_companies.append(company)
        
        db.commit()
        
        # Crear datos financieros para cada empresa
        for company in created_companies:
            for year in [2022, 2023, 2024]:
                # Generar datos financieros realistas
                base_revenue = random.randint(500000, 5000000)
                growth_factor = random.uniform(0.8, 1.3)
                
                if year == 2023:
                    base_revenue *= growth_factor
                elif year == 2024:
                    base_revenue *= growth_factor * random.uniform(0.9, 1.2)
                
                expenses = base_revenue * random.uniform(0.6, 0.9)
                assets = base_revenue * random.uniform(0.8, 2.0)
                liabilities = assets * random.uniform(0.2, 0.7)
                cash_flow = base_revenue - expenses + random.randint(-100000, 200000)
                debt_to_equity = liabilities / (assets - liabilities) if (assets - liabilities) > 0 else 0
                
                financial_data = FinancialData(
                    company_id=company.id,
                    year=year,
                    revenue=base_revenue,
                    expenses=expenses,
                    assets=assets,
                    liabilities=liabilities,
                    cash_flow=cash_flow,
                    debt_to_equity=debt_to_equity
                )
                db.add(financial_data)
        
        db.commit()
        
        print("✅ Datos de ejemplo creados exitosamente:")
        print(f"   - {len(companies_data)} empresas")
        print(f"   - {len(companies_data) * 3} registros financieros")
        print("🚀 Sistema listo para demostración")
        
    except Exception as e:
        print(f"❌ Error creando datos: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()
