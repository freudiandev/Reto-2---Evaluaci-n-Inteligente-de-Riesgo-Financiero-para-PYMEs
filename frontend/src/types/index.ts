export interface Company {
  id: number;
  ruc: string;
  name: string;
  sector?: string;
  legal_form?: string;
  foundation_date?: string;
  address?: string;
  phone?: string;
  email?: string;
  website?: string;
  social_media?: Record<string, string>;
  created_at: string;
}

export interface CompanyCreate {
  ruc: string;
  name: string;
  sector?: string;
  legal_form?: string;
  foundation_date?: string;
  address?: string;
  phone?: string;
  email?: string;
  website?: string;
  social_media?: Record<string, string>;
}

export interface CreditApplication {
  id: number;
  company_id: number;
  requested_amount: number;
  purpose: string;
  term_months: number;
  status: ApplicationStatus;
  created_at: string;
}

export interface CreditApplicationCreate {
  company_id: number;
  requested_amount: number;
  purpose: string;
  term_months: number;
}

export interface FinancialStatement {
  id: number;
  company_id: number;
  application_id: number;
  year: number;
  current_assets: number;
  non_current_assets: number;
  total_assets: number;
  current_liabilities: number;
  non_current_liabilities: number;
  total_liabilities: number;
  equity: number;
  total_revenue: number;
  cost_of_goods_sold: number;
  gross_profit: number;
  operating_expenses: number;
  operating_income: number;
  financial_expenses: number;
  net_income: number;
  operating_cash_flow: number;
  investing_cash_flow: number;
  financing_cash_flow: number;
  net_cash_flow: number;
  file_path?: string;
  created_at: string;
}

export interface SocialMediaAnalysis {
  id: number;
  company_id: number;
  application_id: number;
  platform: SocialMediaPlatform;
  url: string;
  followers_count: number;
  following_count: number;
  posts_count: number;
  positive_sentiment_score: number;
  negative_sentiment_score: number;
  neutral_sentiment_score: number;
  overall_sentiment: SentimentType;
  avg_likes_per_post: number;
  avg_comments_per_post: number;
  avg_shares_per_post: number;
  last_post_date?: string;
  posting_frequency: PostingFrequency;
  professional_content_score: number;
  business_relevance_score: number;
  created_at: string;
}

export interface RiskScore {
  id: number;
  company_id: number;
  application_id: number;
  financial_score: number;
  social_media_score: number;
  business_reputation_score: number;
  overall_score: number;
  risk_level: RiskLevel;
  recommended_credit_limit: number;
  recommended_interest_rate: number;
  recommended_term_months: number;
  decision_factors: Record<string, any>;
  risk_factors: string[];
  model_version: string;
  confidence_level: number;
  created_at: string;
}

export interface SimulationScenario {
  id: number;
  company_id: number;
  application_id: number;
  scenario_name: string;
  revenue_change_percent: number;
  expense_change_percent: number;
  social_media_improvement: boolean;
  payment_history_improvement: boolean;
  new_risk_score: number;
  new_risk_level: RiskLevel;
  new_credit_limit: number;
  score_improvement: number;
  created_at: string;
}

export interface FinancialRatios {
  liquidity_ratio: number;
  debt_to_equity: number;
  return_on_assets: number;
  return_on_equity: number;
  profit_margin: number;
  asset_turnover: number;
}

export interface DashboardData {
  total_applications: number;
  approved_applications: number;
  rejected_applications: number;
  pending_applications: number;
  average_risk_score: number;
  total_credit_amount: number;
  sector_distribution: Record<string, number>;
  risk_level_distribution: Record<string, number>;
}

export interface RiskAnalysisReport {
  company: Company;
  application: CreditApplication;
  financial_statement?: FinancialStatement;
  social_media_analysis: SocialMediaAnalysis[];
  risk_score: RiskScore;
  financial_ratios: FinancialRatios;
  recommendations: string[];
  warnings: string[];
  generated_at: string;
}

// Enums
export type ApplicationStatus = 'pending' | 'approved' | 'rejected' | 'in_review';
export type RiskLevel = 'low' | 'medium' | 'high';
export type SocialMediaPlatform = 'facebook' | 'instagram' | 'linkedin' | 'twitter' | 'tiktok';
export type SentimentType = 'positive' | 'negative' | 'neutral';
export type PostingFrequency = 'daily' | 'weekly' | 'monthly' | 'rarely';

// API Response types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

// Form types
export interface SocialMediaAnalysisRequest {
  company_id: number;
  application_id: number;
  platform: SocialMediaPlatform;
  url: string;
}

export interface SimulationRequest {
  company_id: number;
  application_id: number;
  scenario_name: string;
  revenue_change_percent?: number;
  expense_change_percent?: number;
  social_media_improvement?: boolean;
  payment_history_improvement?: boolean;
}
