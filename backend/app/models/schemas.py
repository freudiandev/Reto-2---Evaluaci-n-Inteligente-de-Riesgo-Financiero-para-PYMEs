from pydantic import BaseModel, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class ApplicationStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    IN_REVIEW = "in_review"

class SocialMediaPlatform(str, Enum):
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    LINKEDIN = "linkedin"
    TWITTER = "twitter"
    TIKTOK = "tiktok"

# Datos para crear empresas
class CompanyCreate(BaseModel):
    ruc: str
    name: str
    sector: Optional[str] = None
    legal_form: Optional[str] = None
    foundation_date: Optional[datetime] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    social_media: Optional[Dict[str, str]] = {}

    @validator('ruc')
    def validate_ruc(cls, v):
        if len(v) != 13:
            raise ValueError('El RUC debe tener 13 dígitos')
        if not v.isdigit():
            raise ValueError('El RUC debe contener solo números')
        return v

# Datos para solicitudes de crédito
class CreditApplicationCreate(BaseModel):
    company_id: int
    requested_amount: float
    purpose: str
    term_months: int

    @validator('requested_amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('El monto solicitado debe ser mayor a 0')
        return v

    @validator('term_months')
    def validate_term(cls, v):
        if v <= 0 or v > 360:
            raise ValueError('El plazo debe estar entre 1 y 360 meses')
        return v

# Estados financieros
class FinancialStatementCreate(BaseModel):
    company_id: int
    application_id: int
    year: int
    current_assets: float = 0
    non_current_assets: float = 0
    current_liabilities: float = 0
    non_current_liabilities: float = 0
    equity: float = 0
    total_revenue: float = 0
    cost_of_goods_sold: float = 0
    operating_expenses: float = 0
    financial_expenses: float = 0
    operating_cash_flow: float = 0
    investing_cash_flow: float = 0
    financing_cash_flow: float = 0

# Análisis de redes sociales
class SocialMediaAnalysisRequest(BaseModel):
    company_id: int
    application_id: int
    platform: SocialMediaPlatform
    url: str

# Respuestas de la API
class CompanyResponse(BaseModel):
    id: int
    ruc: str
    name: str
    sector: Optional[str]
    legal_form: Optional[str]
    foundation_date: Optional[datetime]
    address: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    website: Optional[str]
    social_media: Optional[Dict[str, str]]
    created_at: datetime

    class Config:
        from_attributes = True

class CreditApplicationResponse(BaseModel):
    id: int
    company_id: int
    requested_amount: float
    purpose: str
    term_months: int
    status: ApplicationStatus
    created_at: datetime

    class Config:
        from_attributes = True

class FinancialStatementResponse(BaseModel):
    id: int
    company_id: int
    application_id: int
    year: int
    total_assets: float
    total_liabilities: float
    equity: float
    total_revenue: float
    net_income: float
    net_cash_flow: float
    created_at: datetime

    class Config:
        from_attributes = True

class SocialMediaAnalysisResponse(BaseModel):
    id: int
    company_id: int
    application_id: int
    platform: str
    url: str
    followers_count: int
    posts_count: int
    overall_sentiment: str
    professional_content_score: float
    business_relevance_score: float
    created_at: datetime

    class Config:
        from_attributes = True

class RiskScoreResponse(BaseModel):
    id: int
    company_id: int
    application_id: int
    financial_score: float
    social_media_score: float
    business_reputation_score: float
    overall_score: float
    risk_level: RiskLevel
    recommended_credit_limit: float
    recommended_interest_rate: float
    recommended_term_months: int
    decision_factors: Dict[str, Any]
    risk_factors: List[str]
    confidence_level: float
    created_at: datetime

    class Config:
        from_attributes = True

class SimulationRequest(BaseModel):
    company_id: int
    application_id: int
    scenario_name: str
    revenue_change_percent: float = 0
    expense_change_percent: float = 0
    social_media_improvement: bool = False
    payment_history_improvement: bool = False

# Respuesta de simulaciones
class SimulationResponse(BaseModel):
    id: int
    scenario_name: str
    revenue_change_percent: float
    expense_change_percent: float
    social_media_improvement: bool
    payment_history_improvement: bool
    new_risk_score: float
    new_risk_level: RiskLevel
    new_credit_limit: float
    score_improvement: float
    created_at: datetime

    class Config:
        from_attributes = True

# Modelos para reportes
class FinancialRatios(BaseModel):
    liquidity_ratio: float
    debt_to_equity: float
    return_on_assets: float
    return_on_equity: float
    profit_margin: float
    asset_turnover: float

class RiskAnalysisReport(BaseModel):
    company: CompanyResponse
    application: CreditApplicationResponse
    financial_statement: Optional[FinancialStatementResponse]
    social_media_analysis: List[SocialMediaAnalysisResponse]
    risk_score: RiskScoreResponse
    financial_ratios: FinancialRatios
    recommendations: List[str]
    warnings: List[str]

class DashboardData(BaseModel):
    total_applications: int
    approved_applications: int
    rejected_applications: int
    pending_applications: int
    average_risk_score: float
    total_credit_amount: float
    sector_distribution: Dict[str, int]
    risk_level_distribution: Dict[str, int]
