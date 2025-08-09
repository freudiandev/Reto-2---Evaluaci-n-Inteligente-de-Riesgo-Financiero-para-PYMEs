import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, mean_squared_error
import joblib
from typing import Dict, List, Tuple, Optional
import os
from datetime import datetime
import json

class RiskScoringModel:
    """Modelo de IA para scoring de riesgo financiero de PYMEs"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.feature_importance = {}
        self.is_trained = False
        
        # Definir características que usa el modelo
        self.financial_features = [
            'current_ratio', 'debt_to_equity', 'return_on_assets', 'return_on_equity',
            'profit_margin', 'asset_turnover', 'revenue_growth', 'cash_flow_ratio'
        ]
        
        self.social_features = [
            'followers_count', 'posts_count', 'engagement_rate', 'sentiment_score',
            'professional_content_score', 'posting_frequency_score'
        ]
        
        self.business_features = [
            'years_in_business', 'sector_risk_score', 'employee_count',
            'has_website', 'social_media_presence', 'business_verification'
        ]
        
        self.all_features = self.financial_features + self.social_features + self.business_features

    def prepare_features(self, financial_data: Dict, social_data: Dict, business_data: Dict) -> Dict:
        """Preparar características para el modelo"""
        features = {}
        
        # Características financieras
        features.update(self._calculate_financial_ratios(financial_data))
        
        # Características de redes sociales
        features.update(self._calculate_social_scores(social_data))
        
        # Características del negocio
        features.update(self._calculate_business_scores(business_data))
        
        # Rellenar características faltantes con valores por defecto
        for feature in self.all_features:
            if feature not in features:
                features[feature] = 0.0
        
        return features

    def _calculate_financial_ratios(self, financial_data: Dict) -> Dict:
        """Calcular ratios financieros"""
        ratios = {}
        
        # Obtener datos financieros
        current_assets = financial_data.get('current_assets', 0)
        current_liabilities = financial_data.get('current_liabilities', 0)
        total_assets = financial_data.get('total_assets', 0)
        total_liabilities = financial_data.get('total_liabilities', 0)
        equity = financial_data.get('equity', 0)
        revenue = financial_data.get('total_revenue', 0)
        net_income = financial_data.get('net_income', 0)
        cash_flow = financial_data.get('operating_cash_flow', 0)
        
        # Ratio de liquidez corriente
        ratios['current_ratio'] = current_assets / current_liabilities if current_liabilities > 0 else 0
        
        # Ratio de endeudamiento
        ratios['debt_to_equity'] = total_liabilities / equity if equity > 0 else 0
        
        # Rentabilidad sobre activos
        ratios['return_on_assets'] = net_income / total_assets if total_assets > 0 else 0
        
        # Rentabilidad sobre patrimonio
        ratios['return_on_equity'] = net_income / equity if equity > 0 else 0
        
        # Margen de utilidad
        ratios['profit_margin'] = net_income / revenue if revenue > 0 else 0
        
        # Rotación de activos
        ratios['asset_turnover'] = revenue / total_assets if total_assets > 0 else 0
        
        # Crecimiento de ingresos (simulado)
        ratios['revenue_growth'] = 0.05  # 5% por defecto
        
        # Ratio de flujo de caja
        ratios['cash_flow_ratio'] = cash_flow / current_liabilities if current_liabilities > 0 else 0
        
        return ratios

    def _calculate_social_scores(self, social_data: Dict) -> Dict:
        """Calcular puntuaciones de redes sociales"""
        scores = {}
        
        # Normalizar seguidores (log scale)
        followers = social_data.get('followers_count', 0)
        scores['followers_count'] = min(np.log10(followers + 1) / 6, 1.0)  # Normalizado a 0-1
        
        # Normalizar publicaciones
        posts = social_data.get('posts_count', 0)
        scores['posts_count'] = min(posts / 100, 1.0)  # Normalizado a 0-1
        
        # Engagement rate
        scores['engagement_rate'] = social_data.get('engagement_rate', 0) / 10  # Normalizado a 0-1
        
        # Puntuación de sentimiento
        sentiment = social_data.get('overall_sentiment', 'neutral')
        sentiment_mapping = {'positive': 1.0, 'neutral': 0.5, 'negative': 0.0}
        scores['sentiment_score'] = sentiment_mapping.get(sentiment, 0.5)
        
        # Puntuación de contenido profesional
        scores['professional_content_score'] = social_data.get('professional_content_score', 0.5)
        
        # Frecuencia de publicación
        frequency = social_data.get('posting_frequency', 'weekly')
        frequency_mapping = {'daily': 1.0, 'weekly': 0.8, 'monthly': 0.5, 'rarely': 0.2}
        scores['posting_frequency_score'] = frequency_mapping.get(frequency, 0.5)
        
        return scores

    def _calculate_business_scores(self, business_data: Dict) -> Dict:
        """Calcular puntuaciones del negocio"""
        scores = {}
        
        # Años en el negocio
        foundation_date = business_data.get('foundation_date')
        if foundation_date:
            if isinstance(foundation_date, str):
                try:
                    foundation_date = datetime.strptime(foundation_date, '%Y-%m-%d')
                except:
                    foundation_date = datetime.now()
            years = (datetime.now() - foundation_date).days / 365.25
            scores['years_in_business'] = min(years / 10, 1.0)  # Normalizado a 0-1 (10 años = 1.0)
        else:
            scores['years_in_business'] = 0.1  # Valor por defecto
        
        # Puntuación de riesgo por sector
        sector = business_data.get('sector', '')
        sector_risk_mapping = {
            'tecnología': 0.8,
            'servicios': 0.7,
            'comercio': 0.6,
            'manufactura': 0.5,
            'construcción': 0.4,
            'turismo': 0.3,
            'agricultura': 0.5
        }
        scores['sector_risk_score'] = sector_risk_mapping.get(sector.lower(), 0.5)
        
        # Número de empleados (normalizado)
        employees = business_data.get('employee_count', 1)
        scores['employee_count'] = min(employees / 50, 1.0)  # Normalizado a 0-1
        
        # Presencia web
        scores['has_website'] = 1.0 if business_data.get('website') else 0.0
        
        # Presencia en redes sociales
        social_media = business_data.get('social_media', {})
        scores['social_media_presence'] = min(len(social_media) / 3, 1.0)  # Normalizado a 0-1
        
        # Verificación de negocio
        scores['business_verification'] = 1.0 if business_data.get('verified', False) else 0.5
        
        return scores

    def calculate_risk_score(self, features: Dict) -> Dict:
        """Calcular puntuación de riesgo basada en características"""
        # Pesos para diferentes categorías
        weights = {
            'financial': 0.5,    # 50% peso financiero
            'social': 0.25,      # 25% peso redes sociales
            'business': 0.25     # 25% peso negocio
        }
        
        # Calcular puntuaciones por categoría
        financial_score = self._calculate_category_score(features, self.financial_features)
        social_score = self._calculate_category_score(features, self.social_features)
        business_score = self._calculate_category_score(features, self.business_features)
        
        # Puntuación final ponderada
        overall_score = (
            financial_score * weights['financial'] +
            social_score * weights['social'] +
            business_score * weights['business']
        )
        
        # Convertir a escala 0-100
        overall_score_100 = overall_score * 100
        
        # Determinar nivel de riesgo
        if overall_score_100 >= 70:
            risk_level = 'low'
        elif overall_score_100 >= 40:
            risk_level = 'medium'
        else:
            risk_level = 'high'
        
        # Calcular recomendaciones de crédito
        credit_recommendations = self._calculate_credit_recommendations(
            overall_score_100, risk_level, features
        )
        
        # Identificar factores de decisión
        decision_factors = self._identify_decision_factors(features)
        
        return {
            'financial_score': round(financial_score * 100, 2),
            'social_media_score': round(social_score * 100, 2),
            'business_reputation_score': round(business_score * 100, 2),
            'overall_score': round(overall_score_100, 2),
            'risk_level': risk_level,
            'recommended_credit_limit': credit_recommendations['credit_limit'],
            'recommended_interest_rate': credit_recommendations['interest_rate'],
            'recommended_term_months': credit_recommendations['term_months'],
            'decision_factors': decision_factors,
            'confidence_level': self._calculate_confidence(features)
        }

    def _calculate_category_score(self, features: Dict, feature_list: List[str]) -> float:
        """Calcular puntuación para una categoría de características"""
        scores = []
        for feature in feature_list:
            value = features.get(feature, 0)
            # Normalizar valores extremos
            normalized_value = max(0, min(1, value))
            scores.append(normalized_value)
        
        return np.mean(scores) if scores else 0.0

    def _calculate_credit_recommendations(self, score: float, risk_level: str, features: Dict) -> Dict:
        """Calcular recomendaciones de crédito basadas en el score"""
        revenue = features.get('asset_turnover', 0) * 100000  # Estimación simple
        
        if risk_level == 'low':
            credit_multiplier = 0.3
            base_interest = 12.0
        elif risk_level == 'medium':
            credit_multiplier = 0.2
            base_interest = 18.0
        else:
            credit_multiplier = 0.1
            base_interest = 25.0
        
        # Límite de crédito basado en ingresos estimados
        credit_limit = max(5000, revenue * credit_multiplier)
        
        # Tasa de interés ajustada por score
        interest_rate = base_interest - (score - 50) / 100 * 5
        interest_rate = max(8.0, min(30.0, interest_rate))
        
        # Plazo recomendado
        if risk_level == 'low':
            term_months = 36
        elif risk_level == 'medium':
            term_months = 24
        else:
            term_months = 12
        
        return {
            'credit_limit': round(credit_limit, 2),
            'interest_rate': round(interest_rate, 2),
            'term_months': term_months
        }

    def _identify_decision_factors(self, features: Dict) -> Dict:
        """Identificar factores clave en la decisión"""
        factors = {}
        
        # Factores financieros
        if features.get('current_ratio', 0) > 1.5:
            factors['strong_liquidity'] = 'Buena liquidez corriente'
        elif features.get('current_ratio', 0) < 1.0:
            factors['weak_liquidity'] = 'Liquidez corriente baja'
        
        if features.get('debt_to_equity', 0) > 2.0:
            factors['high_leverage'] = 'Alto nivel de endeudamiento'
        
        if features.get('profit_margin', 0) > 0.1:
            factors['profitable'] = 'Márgenes de utilidad saludables'
        
        # Factores sociales
        if features.get('sentiment_score', 0) > 0.7:
            factors['positive_reputation'] = 'Buena reputación en redes sociales'
        elif features.get('sentiment_score', 0) < 0.3:
            factors['reputation_concerns'] = 'Preocupaciones en reputación online'
        
        # Factores de negocio
        if features.get('years_in_business', 0) > 0.5:
            factors['established_business'] = 'Negocio establecido'
        
        if features.get('social_media_presence', 0) > 0.7:
            factors['strong_digital_presence'] = 'Fuerte presencia digital'
        
        return factors

    def _calculate_confidence(self, features: Dict) -> float:
        """Calcular nivel de confianza del modelo"""
        # Factores que afectan la confianza
        data_completeness = sum(1 for f in self.all_features if features.get(f, 0) > 0) / len(self.all_features)
        
        # Consistencia de datos (ejemplo simple)
        consistency_score = 0.8  # Por defecto
        
        # Confianza final
        confidence = (data_completeness + consistency_score) / 2
        return round(confidence, 3)

    def simulate_scenario(self, base_features: Dict, changes: Dict) -> Dict:
        """Simular escenarios de cambio"""
        # Crear copia de características base
        scenario_features = base_features.copy()
        
        # Aplicar cambios
        if 'revenue_change_percent' in changes:
            change_factor = 1 + (changes['revenue_change_percent'] / 100)
            scenario_features['asset_turnover'] *= change_factor
            scenario_features['profit_margin'] *= change_factor
        
        if 'expense_change_percent' in changes:
            change_factor = 1 + (changes['expense_change_percent'] / 100)
            scenario_features['profit_margin'] /= change_factor
        
        if changes.get('social_media_improvement'):
            scenario_features['sentiment_score'] = min(1.0, scenario_features.get('sentiment_score', 0.5) + 0.2)
            scenario_features['professional_content_score'] = min(1.0, scenario_features.get('professional_content_score', 0.5) + 0.15)
        
        if changes.get('payment_history_improvement'):
            scenario_features['current_ratio'] = min(3.0, scenario_features.get('current_ratio', 1.0) + 0.3)
        
        # Calcular nuevo score
        new_score = self.calculate_risk_score(scenario_features)
        
        return new_score

    def export_model_info(self) -> Dict:
        """Exportar información del modelo"""
        return {
            'model_type': 'Risk Scoring Model',
            'version': '1.0',
            'features_used': self.all_features,
            'feature_categories': {
                'financial': self.financial_features,
                'social': self.social_features,
                'business': self.business_features
            },
            'risk_levels': ['low', 'medium', 'high'],
            'output_range': '0-100',
            'last_updated': datetime.now().isoformat()
        }
