from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from typing import Dict, List, Tuple
import re

# Descargar recursos de NLTK si no están disponibles
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class SentimentAnalyzer:
    """Analizador de sentimientos para redes sociales y texto"""
    
    def __init__(self):
        self.vader_analyzer = SentimentIntensityAnalyzer()
        
        # Palabras clave positivas y negativas específicas para negocios
        self.business_positive_keywords = [
            'excelente', 'recomendado', 'calidad', 'profesional', 'confiable',
            'responsable', 'puntual', 'honesto', 'innovador', 'líder',
            'satisfecho', 'bueno', 'increíble', 'fantástico', 'perfecto'
        ]
        
        self.business_negative_keywords = [
            'malo', 'terrible', 'estafa', 'fraude', 'irresponsable',
            'impuntual', 'deshonesto', 'problema', 'queja', 'deficiente',
            'pésimo', 'horrible', 'desastre', 'nunca más', 'evitar'
        ]

    def analyze_text_sentiment(self, text: str) -> Dict:
        """Analizar sentimiento de un texto"""
        if not text or not text.strip():
            return {
                'positive': 0.0,
                'negative': 0.0,
                'neutral': 1.0,
                'compound': 0.0,
                'overall': 'neutral'
            }
        
        # Análisis con VADER
        vader_scores = self.vader_analyzer.polarity_scores(text)
        
        # Análisis con TextBlob
        blob = TextBlob(text)
        textblob_polarity = blob.sentiment.polarity
        
        # Análisis de palabras clave específicas del negocio
        business_sentiment = self._analyze_business_keywords(text)
        
        # Combinar resultados
        combined_positive = (vader_scores['pos'] + max(0, textblob_polarity) + business_sentiment['positive']) / 3
        combined_negative = (vader_scores['neg'] + max(0, -textblob_polarity) + business_sentiment['negative']) / 3
        combined_neutral = vader_scores['neu']
        
        # Determinar sentimiento general
        if combined_positive > combined_negative and combined_positive > 0.3:
            overall = 'positive'
        elif combined_negative > combined_positive and combined_negative > 0.3:
            overall = 'negative'
        else:
            overall = 'neutral'
        
        return {
            'positive': round(combined_positive, 3),
            'negative': round(combined_negative, 3),
            'neutral': round(combined_neutral, 3),
            'compound': round(vader_scores['compound'], 3),
            'overall': overall,
            'confidence': max(combined_positive, combined_negative, combined_neutral)
        }

    def analyze_social_media_sentiment(self, posts: List[str], comments: List[str] = None) -> Dict:
        """Analizar sentimiento de publicaciones y comentarios de redes sociales"""
        all_text = posts.copy()
        if comments:
            all_text.extend(comments)
        
        if not all_text:
            return {
                'overall_sentiment': 'neutral',
                'positive_score': 0.0,
                'negative_score': 0.0,
                'neutral_score': 1.0,
                'posts_analyzed': 0,
                'sentiment_distribution': {'positive': 0, 'negative': 0, 'neutral': 0}
            }
        
        sentiments = []
        sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0}
        
        for text in all_text:
            sentiment = self.analyze_text_sentiment(text)
            sentiments.append(sentiment)
            sentiment_counts[sentiment['overall']] += 1
        
        # Calcular promedios
        avg_positive = sum(s['positive'] for s in sentiments) / len(sentiments)
        avg_negative = sum(s['negative'] for s in sentiments) / len(sentiments)
        avg_neutral = sum(s['neutral'] for s in sentiments) / len(sentiments)
        
        # Determinar sentimiento general
        if avg_positive > avg_negative and avg_positive > 0.4:
            overall = 'positive'
        elif avg_negative > avg_positive and avg_negative > 0.4:
            overall = 'negative'
        else:
            overall = 'neutral'
        
        return {
            'overall_sentiment': overall,
            'positive_score': round(avg_positive, 3),
            'negative_score': round(avg_negative, 3),
            'neutral_score': round(avg_neutral, 3),
            'posts_analyzed': len(all_text),
            'sentiment_distribution': sentiment_counts
        }

    def _analyze_business_keywords(self, text: str) -> Dict:
        """Analizar palabras clave específicas del contexto de negocios"""
        text_lower = text.lower()
        
        positive_count = sum(1 for keyword in self.business_positive_keywords if keyword in text_lower)
        negative_count = sum(1 for keyword in self.business_negative_keywords if keyword in text_lower)
        
        total_keywords = positive_count + negative_count
        if total_keywords == 0:
            return {'positive': 0.0, 'negative': 0.0}
        
        positive_ratio = positive_count / total_keywords
        negative_ratio = negative_count / total_keywords
        
        return {
            'positive': positive_ratio,
            'negative': negative_ratio
        }

    def extract_business_topics(self, text: str) -> List[str]:
        """Extraer temas relacionados con el negocio del texto"""
        business_topics = [
            'servicio al cliente', 'calidad', 'precio', 'entrega', 'puntualidad',
            'profesionalismo', 'confianza', 'producto', 'atención', 'experiencia',
            'recomendación', 'satisfacción', 'problema', 'solución', 'innovación'
        ]
        
        text_lower = text.lower()
        found_topics = []
        
        for topic in business_topics:
            if topic in text_lower:
                found_topics.append(topic)
        
        return found_topics

class ContentQualityAnalyzer:
    """Analizador de calidad de contenido en redes sociales"""
    
    def __init__(self):
        self.professional_indicators = [
            'empresa', 'servicio', 'producto', 'cliente', 'calidad', 'profesional',
            'experiencia', 'equipo', 'solución', 'innovación', 'tecnología',
            'certificado', 'garantía', 'compromiso', 'excelencia'
        ]
        
        self.spam_indicators = [
            'compra ahora', 'oferta limitada', 'gratis', 'dinero fácil',
            'haz clic aquí', 'urgente', 'último día', 'no pierdas'
        ]

    def analyze_content_quality(self, text: str) -> Dict:
        """Analizar la calidad del contenido"""
        if not text or not text.strip():
            return {
                'professional_score': 0.0,
                'spam_score': 0.0,
                'readability_score': 0.0,
                'overall_quality': 0.0
            }
        
        text_lower = text.lower()
        words = text_lower.split()
        
        # Calcular puntuación profesional
        professional_count = sum(1 for indicator in self.professional_indicators if indicator in text_lower)
        professional_score = min(professional_count / 5, 1.0)  # Normalizar a 0-1
        
        # Calcular puntuación de spam
        spam_count = sum(1 for indicator in self.spam_indicators if indicator in text_lower)
        spam_score = min(spam_count / 3, 1.0)  # Normalizar a 0-1
        
        # Calcular legibilidad básica
        readability_score = self._calculate_readability(text)
        
        # Puntuación general de calidad
        overall_quality = (professional_score + (1 - spam_score) + readability_score) / 3
        
        return {
            'professional_score': round(professional_score, 3),
            'spam_score': round(spam_score, 3),
            'readability_score': round(readability_score, 3),
            'overall_quality': round(overall_quality, 3)
        }

    def _calculate_readability(self, text: str) -> float:
        """Calcular puntuación básica de legibilidad"""
        if not text:
            return 0.0
        
        sentences = text.count('.') + text.count('!') + text.count('?')
        words = len(text.split())
        
        if sentences == 0 or words == 0:
            return 0.0
        
        # Promedio de palabras por oración
        avg_words_per_sentence = words / sentences
        
        # Puntuación simple: oraciones más cortas = más legible
        if avg_words_per_sentence <= 15:
            return 1.0
        elif avg_words_per_sentence <= 25:
            return 0.7
        else:
            return 0.4

class BusinessReputationAnalyzer:
    """Analizador de reputación empresarial basado en múltiples fuentes"""
    
    def analyze_reputation(self, social_media_data: Dict, review_data: Dict = None) -> Dict:
        """Analizar reputación general del negocio"""
        reputation_score = 0.0
        factors = []
        
        # Analizar datos de redes sociales
        if social_media_data:
            social_score = self._analyze_social_reputation(social_media_data)
            reputation_score += social_score * 0.7  # 70% del peso
            factors.append(f"Redes sociales: {social_score:.2f}")
        
        # Analizar reseñas si están disponibles
        if review_data:
            review_score = self._analyze_review_reputation(review_data)
            reputation_score += review_score * 0.3  # 30% del peso
            factors.append(f"Reseñas: {review_score:.2f}")
        
        # Determinar nivel de reputación
        if reputation_score >= 0.7:
            reputation_level = 'excellent'
        elif reputation_score >= 0.5:
            reputation_level = 'good'
        elif reputation_score >= 0.3:
            reputation_level = 'fair'
        else:
            reputation_level = 'poor'
        
        return {
            'reputation_score': round(reputation_score, 3),
            'reputation_level': reputation_level,
            'contributing_factors': factors,
            'recommendations': self._generate_reputation_recommendations(reputation_score)
        }

    def _analyze_social_reputation(self, social_data: Dict) -> float:
        """Analizar reputación basada en redes sociales"""
        score = 0.0
        
        # Factores de engagement
        followers = social_data.get('followers_count', 0)
        posts = social_data.get('posts_count', 0)
        
        # Puntuación por número de seguidores (normalizada)
        if followers > 1000:
            follower_score = 1.0
        elif followers > 500:
            follower_score = 0.8
        elif followers > 100:
            follower_score = 0.6
        else:
            follower_score = 0.4
        
        # Puntuación por actividad
        if posts > 50:
            activity_score = 1.0
        elif posts > 20:
            activity_score = 0.8
        elif posts > 5:
            activity_score = 0.6
        else:
            activity_score = 0.4
        
        # Sentimiento general
        sentiment = social_data.get('overall_sentiment', 'neutral')
        if sentiment == 'positive':
            sentiment_score = 1.0
        elif sentiment == 'neutral':
            sentiment_score = 0.6
        else:
            sentiment_score = 0.2
        
        score = (follower_score + activity_score + sentiment_score) / 3
        return score

    def _analyze_review_reputation(self, review_data: Dict) -> float:
        """Analizar reputación basada en reseñas"""
        # Implementación básica para reseñas
        avg_rating = review_data.get('average_rating', 3.0)
        review_count = review_data.get('review_count', 0)
        
        # Normalizar rating (1-5 -> 0-1)
        rating_score = (avg_rating - 1) / 4
        
        # Factor de confianza basado en número de reseñas
        if review_count > 50:
            confidence = 1.0
        elif review_count > 20:
            confidence = 0.8
        elif review_count > 5:
            confidence = 0.6
        else:
            confidence = 0.4
        
        return rating_score * confidence

    def _generate_reputation_recommendations(self, score: float) -> List[str]:
        """Generar recomendaciones para mejorar la reputación"""
        recommendations = []
        
        if score < 0.5:
            recommendations.extend([
                "Mejorar la presencia en redes sociales",
                "Publicar contenido de calidad regularmente",
                "Responder a comentarios y mensajes de manera oportuna",
                "Solicitar reseñas a clientes satisfechos"
            ])
        elif score < 0.7:
            recommendations.extend([
                "Aumentar la frecuencia de publicaciones",
                "Interactuar más con seguidores",
                "Compartir testimonios de clientes"
            ])
        else:
            recommendations.extend([
                "Mantener la excelente presencia digital",
                "Considerar expandir a nuevas plataformas"
            ])
        
        return recommendations
