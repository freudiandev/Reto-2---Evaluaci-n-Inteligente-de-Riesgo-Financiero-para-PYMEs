from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import uuid
from datetime import datetime

from app.services.database import get_db
from app.models.database import Company, CreditApplication, FinancialStatement, SocialMediaAnalysis, RiskScore, SimulationScenario
from app.models.schemas import *
from app.services.social_media_scraper import SocialMediaScraper
from app.services.document_processor import FinancialDocumentProcessor, SuperciasDataExtractor
from app.ai.sentiment_analyzer import SentimentAnalyzer, ContentQualityAnalyzer, BusinessReputationAnalyzer
from app.ai.risk_model import RiskScoringModel
from config import UPLOAD_DIR, MAX_FILE_SIZE

router = APIRouter()

# Inicializar servicios
social_scraper = SocialMediaScraper()
doc_processor = FinancialDocumentProcessor()
supercias_extractor = SuperciasDataExtractor()
sentiment_analyzer = SentimentAnalyzer()
content_analyzer = ContentQualityAnalyzer()
reputation_analyzer = BusinessReputationAnalyzer()
risk_model = RiskScoringModel()

@router.get("/health")
async def health_check():
    """Verificar estado de la API"""
    return {"status": "healthy", "timestamp": datetime.now()}

# === ENDPOINTS DE EMPRESAS ===

@router.post("/companies/", response_model=CompanyResponse)
async def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    """Crear nueva empresa"""
    # Verificar si la empresa ya existe
    existing_company = db.query(Company).filter(Company.ruc == company.ruc).first()
    if existing_company:
        raise HTTPException(status_code=400, detail="La empresa con este RUC ya existe")
    
    # Obtener datos adicionales de Supercias
    supercias_data = supercias_extractor.search_company_by_ruc(company.ruc)
    
    # Crear empresa
    db_company = Company(
        ruc=company.ruc,
        name=company.name,
        sector=company.sector or supercias_data.get('activity', ''),
        legal_form=company.legal_form,
        foundation_date=company.foundation_date,
        address=company.address or supercias_data.get('address', ''),
        phone=company.phone or supercias_data.get('phone', ''),
        email=company.email or supercias_data.get('email', ''),
        website=company.website,
        social_media=company.social_media
    )
    
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    
    return db_company

@router.get("/companies/", response_model=List[CompanyResponse])
async def list_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar empresas"""
    companies = db.query(Company).offset(skip).limit(limit).all()
    return companies

@router.get("/companies/{company_id}", response_model=CompanyResponse)
async def get_company(company_id: int, db: Session = Depends(get_db)):
    """Obtener empresa por ID"""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return company

@router.get("/companies/ruc/{ruc}", response_model=CompanyResponse)
async def get_company_by_ruc(ruc: str, db: Session = Depends(get_db)):
    """Obtener empresa por RUC"""
    company = db.query(Company).filter(Company.ruc == ruc).first()
    if not company:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return company

# === ENDPOINTS DE SOLICITUDES DE CRÉDITO ===

@router.post("/applications/", response_model=CreditApplicationResponse)
async def create_application(application: CreditApplicationCreate, db: Session = Depends(get_db)):
    """Crear nueva solicitud de crédito"""
    # Verificar que la empresa existe
    company = db.query(Company).filter(Company.id == application.company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    
    db_application = CreditApplication(
        company_id=application.company_id,
        requested_amount=application.requested_amount,
        purpose=application.purpose,
        term_months=application.term_months
    )
    
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    
    return db_application

@router.get("/applications/", response_model=List[CreditApplicationResponse])
async def list_applications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar solicitudes de crédito"""
    applications = db.query(CreditApplication).offset(skip).limit(limit).all()
    return applications

@router.get("/applications/{application_id}", response_model=CreditApplicationResponse)
async def get_application(application_id: int, db: Session = Depends(get_db)):
    """Obtener solicitud por ID"""
    application = db.query(CreditApplication).filter(CreditApplication.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    return application

# === ENDPOINTS DE ESTADOS FINANCIEROS ===

@router.post("/financial-statements/upload")
async def upload_financial_statement(
    company_id: int = Form(...),
    application_id: int = Form(...),
    year: int = Form(...),
    file: UploadFile = File(...)
):
    """Subir y procesar estado financiero"""
    
    # Validar tamaño del archivo
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="Archivo demasiado grande")
    
    # Crear directorio de uploads si no existe
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # Generar nombre único para el archivo
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Guardar archivo
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Procesar archivo
    processed_data = doc_processor.process_file(file_path)
    
    if 'error' in processed_data:
        os.remove(file_path)  # Eliminar archivo si hay error
        raise HTTPException(status_code=400, detail=processed_data['error'])
    
    return {
        "message": "Archivo procesado exitosamente",
        "file_path": file_path,
        "processed_data": processed_data
    }

@router.post("/financial-statements/", response_model=FinancialStatementResponse)
async def create_financial_statement(
    statement: FinancialStatementCreate, 
    db: Session = Depends(get_db)
):
    """Crear estado financiero manualmente"""
    db_statement = FinancialStatement(**statement.dict())
    
    # Calcular campos derivados
    db_statement.total_assets = db_statement.current_assets + db_statement.non_current_assets
    db_statement.total_liabilities = db_statement.current_liabilities + db_statement.non_current_liabilities
    db_statement.gross_profit = db_statement.total_revenue - db_statement.cost_of_goods_sold
    db_statement.operating_income = db_statement.gross_profit - db_statement.operating_expenses
    db_statement.net_income = db_statement.operating_income - db_statement.financial_expenses
    db_statement.net_cash_flow = (db_statement.operating_cash_flow + 
                                 db_statement.investing_cash_flow + 
                                 db_statement.financing_cash_flow)
    
    db.add(db_statement)
    db.commit()
    db.refresh(db_statement)
    
    return db_statement

# === ENDPOINTS DE ANÁLISIS DE REDES SOCIALES ===

@router.post("/social-media/analyze")
async def analyze_social_media(
    request: SocialMediaAnalysisRequest,
    db: Session = Depends(get_db)
):
    """Analizar red social de la empresa"""
    
    # Realizar scraping de la red social
    scraping_data = social_scraper.analyze_social_media(request.url)
    
    if 'error' in scraping_data:
        raise HTTPException(status_code=400, detail=scraping_data['error'])
    
    # Analizar sentimientos si hay contenido
    sentiment_data = {}
    if 'posts' in scraping_data:
        posts = scraping_data.get('posts', [])
        comments = scraping_data.get('comments', [])
        sentiment_data = sentiment_analyzer.analyze_social_media_sentiment(posts, comments)
    
    # Analizar calidad del contenido
    content_quality = {}
    if 'bio' in scraping_data or 'description' in scraping_data:
        text_content = scraping_data.get('bio', '') + ' ' + scraping_data.get('description', '')
        content_quality = content_analyzer.analyze_content_quality(text_content)
    
    # Guardar análisis en base de datos
    db_analysis = SocialMediaAnalysis(
        company_id=request.company_id,
        application_id=request.application_id,
        platform=request.platform,
        url=request.url,
        followers_count=scraping_data.get('followers_count', 0),
        following_count=scraping_data.get('following_count', 0),
        posts_count=scraping_data.get('posts_count', 0),
        positive_sentiment_score=sentiment_data.get('positive_score', 0),
        negative_sentiment_score=sentiment_data.get('negative_score', 0),
        neutral_sentiment_score=sentiment_data.get('neutral_score', 0),
        overall_sentiment=sentiment_data.get('overall_sentiment', 'neutral'),
        professional_content_score=content_quality.get('professional_score', 0),
        business_relevance_score=content_quality.get('overall_quality', 0),
        raw_data=scraping_data
    )
    
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    
    return {
        "message": "Análisis completado",
        "analysis_id": db_analysis.id,
        "scraping_data": scraping_data,
        "sentiment_analysis": sentiment_data,
        "content_quality": content_quality
    }

# === ENDPOINTS DE SCORING DE RIESGO ===

@router.post("/risk-score/calculate/{application_id}")
async def calculate_risk_score(application_id: int, db: Session = Depends(get_db)):
    """Calcular score de riesgo para una solicitud"""
    
    # Obtener solicitud
    application = db.query(CreditApplication).filter(CreditApplication.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    
    # Obtener empresa
    company = db.query(Company).filter(Company.id == application.company_id).first()
    
    # Obtener estado financiero más reciente
    financial_statement = db.query(FinancialStatement).filter(
        FinancialStatement.application_id == application_id
    ).order_by(FinancialStatement.year.desc()).first()
    
    # Obtener análisis de redes sociales
    social_analyses = db.query(SocialMediaAnalysis).filter(
        SocialMediaAnalysis.application_id == application_id
    ).all()
    
    # Preparar datos para el modelo
    financial_data = {}
    if financial_statement:
        financial_data = {
            'current_assets': financial_statement.current_assets,
            'non_current_assets': financial_statement.non_current_assets,
            'current_liabilities': financial_statement.current_liabilities,
            'non_current_liabilities': financial_statement.non_current_liabilities,
            'equity': financial_statement.equity,
            'total_revenue': financial_statement.total_revenue,
            'net_income': financial_statement.net_income,
            'operating_cash_flow': financial_statement.operating_cash_flow,
            'total_assets': financial_statement.total_assets,
            'total_liabilities': financial_statement.total_liabilities
        }
    
    # Consolidar datos de redes sociales
    social_data = {}
    if social_analyses:
        total_followers = sum(analysis.followers_count for analysis in social_analyses)
        total_posts = sum(analysis.posts_count for analysis in social_analyses)
        avg_sentiment = sum(analysis.positive_sentiment_score for analysis in social_analyses) / len(social_analyses)
        avg_professional = sum(analysis.professional_content_score for analysis in social_analyses) / len(social_analyses)
        
        social_data = {
            'followers_count': total_followers,
            'posts_count': total_posts,
            'overall_sentiment': 'positive' if avg_sentiment > 0.6 else 'neutral' if avg_sentiment > 0.3 else 'negative',
            'professional_content_score': avg_professional,
            'engagement_rate': 3.0,  # Valor por defecto
            'posting_frequency': 'weekly'
        }
    
    # Datos del negocio
    business_data = {
        'foundation_date': company.foundation_date,
        'sector': company.sector,
        'website': company.website,
        'social_media': company.social_media,
        'employee_count': 10,  # Valor estimado por defecto
        'verified': True
    }
    
    # Preparar características para el modelo
    features = risk_model.prepare_features(financial_data, social_data, business_data)
    
    # Calcular score de riesgo
    risk_score_result = risk_model.calculate_risk_score(features)
    
    # Guardar resultado en base de datos
    db_risk_score = RiskScore(
        company_id=application.company_id,
        application_id=application_id,
        financial_score=risk_score_result['financial_score'],
        social_media_score=risk_score_result['social_media_score'],
        business_reputation_score=risk_score_result['business_reputation_score'],
        overall_score=risk_score_result['overall_score'],
        risk_level=risk_score_result['risk_level'],
        recommended_credit_limit=risk_score_result['recommended_credit_limit'],
        recommended_interest_rate=risk_score_result['recommended_interest_rate'],
        recommended_term_months=risk_score_result['recommended_term_months'],
        decision_factors=risk_score_result['decision_factors'],
        risk_factors=list(risk_score_result['decision_factors'].values()),
        model_version="1.0",
        confidence_level=risk_score_result['confidence_level']
    )
    
    db.add(db_risk_score)
    db.commit()
    db.refresh(db_risk_score)
    
    return {
        "risk_score_id": db_risk_score.id,
        "result": risk_score_result,
        "features_used": features
    }

# === ENDPOINTS DE SIMULACIONES ===

@router.post("/simulations/", response_model=SimulationResponse)
async def create_simulation(simulation: SimulationRequest, db: Session = Depends(get_db)):
    """Crear simulación de escenario"""
    
    # Obtener el último score de riesgo para esta solicitud
    latest_risk_score = db.query(RiskScore).filter(
        RiskScore.application_id == simulation.application_id
    ).order_by(RiskScore.created_at.desc()).first()
    
    if not latest_risk_score:
        raise HTTPException(status_code=404, detail="No se encontró score de riesgo previo")
    
    # Obtener datos base para la simulación
    # (Aquí deberías obtener las características originales del modelo)
    # Por simplicidad, usamos datos simulados
    base_features = {
        'current_ratio': 1.2,
        'debt_to_equity': 0.8,
        'return_on_assets': 0.05,
        'profit_margin': 0.08,
        'sentiment_score': 0.6,
        'professional_content_score': 0.7,
        'years_in_business': 0.5,
        'social_media_presence': 0.6
    }
    
    # Aplicar cambios del escenario
    changes = {
        'revenue_change_percent': simulation.revenue_change_percent,
        'expense_change_percent': simulation.expense_change_percent,
        'social_media_improvement': simulation.social_media_improvement,
        'payment_history_improvement': simulation.payment_history_improvement
    }
    
    # Simular nuevo score
    new_score_result = risk_model.simulate_scenario(base_features, changes)
    
    # Calcular mejora
    score_improvement = new_score_result['overall_score'] - latest_risk_score.overall_score
    
    # Guardar simulación
    db_simulation = SimulationScenario(
        company_id=simulation.company_id,
        application_id=simulation.application_id,
        scenario_name=simulation.scenario_name,
        revenue_change_percent=simulation.revenue_change_percent,
        expense_change_percent=simulation.expense_change_percent,
        social_media_improvement=simulation.social_media_improvement,
        payment_history_improvement=simulation.payment_history_improvement,
        new_risk_score=new_score_result['overall_score'],
        new_risk_level=new_score_result['risk_level'],
        new_credit_limit=new_score_result['recommended_credit_limit'],
        score_improvement=score_improvement
    )
    
    db.add(db_simulation)
    db.commit()
    db.refresh(db_simulation)
    
    return db_simulation

# === ENDPOINTS DE DASHBOARD ===

@router.get("/dashboard/summary")
async def get_dashboard_summary(db: Session = Depends(get_db)):
    """Obtener resumen para dashboard"""
    
    # Estadísticas generales
    total_applications = db.query(CreditApplication).count()
    approved_applications = db.query(CreditApplication).filter(CreditApplication.status == "approved").count()
    rejected_applications = db.query(CreditApplication).filter(CreditApplication.status == "rejected").count()
    pending_applications = db.query(CreditApplication).filter(CreditApplication.status == "pending").count()
    
    # Promedio de score de riesgo
    risk_scores = db.query(RiskScore).all()
    avg_risk_score = sum(score.overall_score for score in risk_scores) / len(risk_scores) if risk_scores else 0
    
    # Total de crédito solicitado
    total_credit = sum(app.requested_amount for app in db.query(CreditApplication).all())
    
    # Distribución por sector
    companies = db.query(Company).all()
    sector_distribution = {}
    for company in companies:
        sector = company.sector or 'No especificado'
        sector_distribution[sector] = sector_distribution.get(sector, 0) + 1
    
    # Distribución por nivel de riesgo
    risk_level_distribution = {}
    for score in risk_scores:
        level = score.risk_level
        risk_level_distribution[level] = risk_level_distribution.get(level, 0) + 1
    
    return {
        "total_applications": total_applications,
        "approved_applications": approved_applications,
        "rejected_applications": rejected_applications,
        "pending_applications": pending_applications,
        "average_risk_score": round(avg_risk_score, 2),
        "total_credit_amount": total_credit,
        "sector_distribution": sector_distribution,
        "risk_level_distribution": risk_level_distribution
    }

@router.get("/reports/risk-analysis/{application_id}")
async def get_risk_analysis_report(application_id: int, db: Session = Depends(get_db)):
    """Generar reporte completo de análisis de riesgo"""
    
    # Obtener todos los datos relacionados
    application = db.query(CreditApplication).filter(CreditApplication.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    
    company = db.query(Company).filter(Company.id == application.company_id).first()
    financial_statement = db.query(FinancialStatement).filter(
        FinancialStatement.application_id == application_id
    ).order_by(FinancialStatement.year.desc()).first()
    
    social_analyses = db.query(SocialMediaAnalysis).filter(
        SocialMediaAnalysis.application_id == application_id
    ).all()
    
    risk_score = db.query(RiskScore).filter(
        RiskScore.application_id == application_id
    ).order_by(RiskScore.created_at.desc()).first()
    
    # Calcular ratios financieros
    financial_ratios = {}
    if financial_statement:
        financial_ratios = {
            'liquidity_ratio': financial_statement.current_assets / financial_statement.current_liabilities if financial_statement.current_liabilities > 0 else 0,
            'debt_to_equity': financial_statement.total_liabilities / financial_statement.equity if financial_statement.equity > 0 else 0,
            'return_on_assets': financial_statement.net_income / financial_statement.total_assets if financial_statement.total_assets > 0 else 0,
            'return_on_equity': financial_statement.net_income / financial_statement.equity if financial_statement.equity > 0 else 0,
            'profit_margin': financial_statement.net_income / financial_statement.total_revenue if financial_statement.total_revenue > 0 else 0,
            'asset_turnover': financial_statement.total_revenue / financial_statement.total_assets if financial_statement.total_assets > 0 else 0
        }
    
    # Generar recomendaciones
    recommendations = []
    warnings = []
    
    if risk_score:
        if risk_score.overall_score >= 70:
            recommendations.append("Excelente candidato para crédito")
            recommendations.append("Considerar límites de crédito preferenciales")
        elif risk_score.overall_score >= 40:
            recommendations.append("Candidato aceptable con monitoreo")
            warnings.append("Revisar garantías adicionales")
        else:
            warnings.append("Alto riesgo - requiere análisis detallado")
            warnings.append("Considerar garantías robustas")
    
    return {
        "company": company,
        "application": application,
        "financial_statement": financial_statement,
        "social_media_analysis": social_analyses,
        "risk_score": risk_score,
        "financial_ratios": financial_ratios,
        "recommendations": recommendations,
        "warnings": warnings,
        "generated_at": datetime.now()
    }
