from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    ruc = Column(String(13), unique=True, index=True)  # RUC ecuatoriano
    name = Column(String(255), nullable=False)
    sector = Column(String(100))
    legal_form = Column(String(50))  # SA, SRL, etc.
    foundation_date = Column(DateTime)
    address = Column(Text)
    phone = Column(String(20))
    email = Column(String(100))
    website = Column(String(255))
    social_media = Column(JSON)  # URLs de redes sociales
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class CreditApplication(Base):
    __tablename__ = "credit_applications"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, index=True)
    requested_amount = Column(Float, nullable=False)
    purpose = Column(Text)  # Propósito del crédito
    term_months = Column(Integer)  # Plazo en meses
    status = Column(String(20), default="pending")  # pending, approved, rejected
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class FinancialStatement(Base):
    __tablename__ = "financial_statements"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, index=True)
    application_id = Column(Integer, index=True)
    year = Column(Integer, nullable=False)
    
    # Estado de Situación Financiera
    current_assets = Column(Float, default=0)
    non_current_assets = Column(Float, default=0)
    total_assets = Column(Float, default=0)
    current_liabilities = Column(Float, default=0)
    non_current_liabilities = Column(Float, default=0)
    total_liabilities = Column(Float, default=0)
    equity = Column(Float, default=0)
    
    # Estado de Resultados
    total_revenue = Column(Float, default=0)
    cost_of_goods_sold = Column(Float, default=0)
    gross_profit = Column(Float, default=0)
    operating_expenses = Column(Float, default=0)
    operating_income = Column(Float, default=0)
    financial_expenses = Column(Float, default=0)
    net_income = Column(Float, default=0)
    
    # Flujo de Caja
    operating_cash_flow = Column(Float, default=0)
    investing_cash_flow = Column(Float, default=0)
    financing_cash_flow = Column(Float, default=0)
    net_cash_flow = Column(Float, default=0)
    
    file_path = Column(String(500))  # Ruta del archivo subido
    created_at = Column(DateTime, default=func.now())

class SocialMediaAnalysis(Base):
    __tablename__ = "social_media_analysis"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, index=True)
    application_id = Column(Integer, index=True)
    platform = Column(String(50))  # facebook, instagram, linkedin, etc.
    url = Column(String(500))
    
    # Métricas básicas
    followers_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)
    posts_count = Column(Integer, default=0)
    
    # Análisis de sentimientos
    positive_sentiment_score = Column(Float, default=0)
    negative_sentiment_score = Column(Float, default=0)
    neutral_sentiment_score = Column(Float, default=0)
    overall_sentiment = Column(String(20))  # positive, negative, neutral
    
    # Engagement y actividad
    avg_likes_per_post = Column(Float, default=0)
    avg_comments_per_post = Column(Float, default=0)
    avg_shares_per_post = Column(Float, default=0)
    last_post_date = Column(DateTime)
    posting_frequency = Column(String(20))  # daily, weekly, monthly, rarely
    
    # Contenido y calidad
    professional_content_score = Column(Float, default=0)
    business_relevance_score = Column(Float, default=0)
    
    raw_data = Column(JSON)  # Datos en bruto del scraping
    created_at = Column(DateTime, default=func.now())

class RiskScore(Base):
    __tablename__ = "risk_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, index=True)
    application_id = Column(Integer, index=True)
    
    # Puntuaciones por categoría
    financial_score = Column(Float, default=0)  # 0-100
    social_media_score = Column(Float, default=0)  # 0-100
    business_reputation_score = Column(Float, default=0)  # 0-100
    
    # Puntuación final
    overall_score = Column(Float, default=0)  # 0-100
    risk_level = Column(String(20))  # low, medium, high
    
    # Recomendaciones
    recommended_credit_limit = Column(Float, default=0)
    recommended_interest_rate = Column(Float, default=0)
    recommended_term_months = Column(Integer, default=0)
    
    # Factores de decisión
    decision_factors = Column(JSON)  # Factores que influyeron en la decisión
    risk_factors = Column(JSON)  # Factores de riesgo identificados
    
    # Metadatos del modelo
    model_version = Column(String(20))
    confidence_level = Column(Float, default=0)  # Confianza del modelo 0-1
    
    created_at = Column(DateTime, default=func.now())

class SimulationScenario(Base):
    __tablename__ = "simulation_scenarios"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, index=True)
    application_id = Column(Integer, index=True)
    scenario_name = Column(String(100))
    
    # Cambios simulados
    revenue_change_percent = Column(Float, default=0)
    expense_change_percent = Column(Float, default=0)
    social_media_improvement = Column(Boolean, default=False)
    payment_history_improvement = Column(Boolean, default=False)
    
    # Resultados de la simulación
    new_risk_score = Column(Float, default=0)
    new_risk_level = Column(String(20))
    new_credit_limit = Column(Float, default=0)
    score_improvement = Column(Float, default=0)
    
    created_at = Column(DateTime, default=func.now())
