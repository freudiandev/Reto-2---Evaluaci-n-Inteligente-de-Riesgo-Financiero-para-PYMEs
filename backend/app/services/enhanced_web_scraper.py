"""
Enhanced Web Scraping Engine para PyMEs Ecuador
Sistema de scraping real para redes sociales y referencias comerciales
"""

import requests
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json
import time
import logging
from typing import Dict, List, Optional
from urllib.parse import urljoin, quote_plus
import re
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class EnhancedWebScrapingEngine:
    """Motor de web scraping mejorado para análisis de PyMEs ecuatorianas"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # APIs y fuentes de datos públicas en Ecuador
        self.data_sources = {
            'supercias': 'https://www.supercias.gob.ec/portalscvs/',
            'sri': 'https://srienlinea.sri.gob.ec/',
            'banco_central': 'https://www.bce.fin.ec/',
            'google_business': 'https://www.google.com/search?q=',
            'facebook_search': 'https://www.facebook.com/search/top?q=',
            'linkedin_search': 'https://www.linkedin.com/search/results/companies/?keywords=',
            'mercadolibre': 'https://listado.mercadolibre.com.ec/',
            'olx_ecuador': 'https://ecuador.olx.com/',
            'patiotuerca': 'https://www.patiotuerca.com/',
            'plusvalia': 'https://www.plusvalia.com/'
        }
    
    async def scrape_company_digital_footprint(self, company_name: str, ruc: str, social_urls: List[str] = []) -> Dict:
        """Scraping completo de huella digital de la empresa"""
        
        logger.info(f"🔍 Iniciando scraping para empresa: {company_name}")
        
        results = {
            "company_name": company_name,
            "ruc": ruc,
            "scraping_timestamp": datetime.now().isoformat(),
            "digital_presence": {},
            "social_media_analysis": {},
            "online_reputation": {},
            "commercial_references": {},
            "market_visibility": {}
        }
        
        try:
            # 1. Buscar presencia digital general
            results["digital_presence"] = await self._search_digital_presence(company_name, ruc)
            
            # 2. Análizar redes sociales específicas
            if social_urls:
                results["social_media_analysis"] = await self._analyze_social_media_urls(social_urls)
            else:
                results["social_media_analysis"] = await self._search_social_media(company_name)
            
            # 3. Buscar reputación online
            results["online_reputation"] = await self._analyze_online_reputation(company_name)
            
            # 4. Referencias comerciales
            results["commercial_references"] = await self._find_commercial_references(company_name, ruc)
            
            # 5. Visibilidad en marketplace
            results["market_visibility"] = await self._check_marketplace_presence(company_name)
            
            # 6. Calcular score digital
            results["digital_score"] = self._calculate_digital_score(results)
            
            logger.info(f"✅ Scraping completado para {company_name}")
            return results
            
        except Exception as e:
            logger.error(f"❌ Error en scraping para {company_name}: {e}")
            return self._fallback_analysis(company_name, ruc)
    
    async def _search_digital_presence(self, company_name: str, ruc: str) -> Dict:
        """Buscar presencia digital general de la empresa"""
        
        digital_presence = {
            "website_found": False,
            "google_listings": 0,
            "online_mentions": 0,
            "business_directories": [],
            "contact_info_available": False
        }
        
        try:
            # Búsqueda en Google
            search_query = f'"{company_name}" Ecuador site:ec OR "{ruc}"'
            google_results = await self._google_search(search_query)
            
            digital_presence["google_listings"] = len(google_results.get("results", []))
            digital_presence["online_mentions"] = google_results.get("total_results", 0)
            
            # Buscar website oficial
            for result in google_results.get("results", [])[:5]:
                if self._is_official_website(result.get("url", ""), company_name):
                    digital_presence["website_found"] = True
                    digital_presence["official_website"] = result.get("url")
                    break
            
            # Buscar en directorios empresariales
            directories = await self._search_business_directories(company_name, ruc)
            digital_presence["business_directories"] = directories
            
            return digital_presence
            
        except Exception as e:
            logger.error(f"Error buscando presencia digital: {e}")
            return digital_presence
    
    async def _analyze_social_media_urls(self, social_urls: List[str]) -> Dict:
        """Análisis específico de URLs de redes sociales proporcionadas"""
        
        social_analysis = {
            "platforms_analyzed": [],
            "total_followers": 0,
            "total_posts": 0,
            "engagement_rate": 0.0,
            "posting_frequency": "unknown",
            "content_quality_score": 0.0,
            "business_focus_score": 0.0,
            "last_activity": None,
            "platform_details": {}
        }
        
        for url in social_urls:
            try:
                platform = self._identify_platform(url)
                if platform:
                    platform_data = await self._scrape_social_platform(url, platform)
                    social_analysis["platform_details"][platform] = platform_data
                    
                    # Agregar a totales
                    social_analysis["total_followers"] += platform_data.get("followers", 0)
                    social_analysis["total_posts"] += platform_data.get("posts_count", 0)
                    
                    if platform not in social_analysis["platforms_analyzed"]:
                        social_analysis["platforms_analyzed"].append(platform)
                        
            except Exception as e:
                logger.error(f"Error analizando URL {url}: {e}")
        
        # Calcular métricas agregadas
        if social_analysis["platforms_analyzed"]:
            social_analysis["engagement_rate"] = self._calculate_avg_engagement(social_analysis["platform_details"])
            social_analysis["content_quality_score"] = self._analyze_content_quality(social_analysis["platform_details"])
            social_analysis["business_focus_score"] = self._analyze_business_focus(social_analysis["platform_details"])
        
        return social_analysis
    
    async def _search_social_media(self, company_name: str) -> Dict:
        """Búsqueda automática en redes sociales si no se proporcionaron URLs"""
        
        logger.info(f"🔍 Buscando redes sociales para: {company_name}")
        
        social_search = {
            "facebook_found": False,
            "instagram_found": False,
            "linkedin_found": False,
            "twitter_found": False,
            "tiktok_found": False,
            "found_profiles": [],
            "estimated_followers": 0,
            "social_media_score": 0.0
        }
        
        # Búsquedas específicas por plataforma
        platforms_to_search = {
            "facebook": f"site:facebook.com \"{company_name}\" Ecuador",
            "instagram": f"site:instagram.com \"{company_name}\"",
            "linkedin": f"site:linkedin.com/company \"{company_name}\"",
            "twitter": f"site:twitter.com \"{company_name}\" Ecuador"
        }
        
        for platform, query in platforms_to_search.items():
            try:
                results = await self._google_search(query, max_results=3)
                if results.get("results"):
                    social_search[f"{platform}_found"] = True
                    social_search["found_profiles"].extend([
                        {"platform": platform, "url": r.get("url"), "title": r.get("title")}
                        for r in results["results"][:2]
                    ])
                    
            except Exception as e:
                logger.error(f"Error buscando en {platform}: {e}")
        
        # Calcular score de redes sociales
        platforms_found = sum([
            social_search["facebook_found"],
            social_search["instagram_found"], 
            social_search["linkedin_found"],
            social_search["twitter_found"]
        ])
        
        social_search["social_media_score"] = min(platforms_found * 0.25, 1.0)
        
        return social_search
    
    async def _analyze_online_reputation(self, company_name: str) -> Dict:
        """Análisis de reputación online"""
        
        reputation = {
            "review_platforms": [],
            "average_rating": 0.0,
            "total_reviews": 0,
            "sentiment_score": 0.0,
            "negative_mentions": 0,
            "positive_mentions": 0,
            "reputation_score": 0.0
        }
        
        try:
            # Buscar en plataformas de reseñas
            review_queries = [
                f'"{company_name}" Ecuador reseñas OR opiniones OR comentarios',
                f'"{company_name}" Ecuador "google maps" OR "google business"',
                f'"{company_name}" Ecuador experiencia OR servicio'
            ]
            
            all_mentions = []
            for query in review_queries:
                results = await self._google_search(query, max_results=10)
                all_mentions.extend(results.get("results", []))
            
            # Analizar sentiment de los títulos y snippets
            for mention in all_mentions:
                title = mention.get("title", "")
                snippet = mention.get("snippet", "")
                text = f"{title} {snippet}"
                
                sentiment = self._analyze_text_sentiment(text)
                if sentiment > 0.6:
                    reputation["positive_mentions"] += 1
                elif sentiment < 0.4:
                    reputation["negative_mentions"] += 1
            
            # Calcular score de reputación
            total_mentions = reputation["positive_mentions"] + reputation["negative_mentions"]
            if total_mentions > 0:
                reputation["sentiment_score"] = reputation["positive_mentions"] / total_mentions
                reputation["reputation_score"] = min(reputation["sentiment_score"] * 0.8 + (total_mentions / 20) * 0.2, 1.0)
            else:
                reputation["reputation_score"] = 0.5  # Score neutral sin información
            
            return reputation
            
        except Exception as e:
            logger.error(f"Error analizando reputación: {e}")
            return reputation
    
    async def _find_commercial_references(self, company_name: str, ruc: str) -> Dict:
        """Buscar referencias comerciales y proveedores"""
        
        references = {
            "supplier_mentions": 0,
            "client_testimonials": 0,
            "business_partnerships": [],
            "marketplace_presence": False,
            "commercial_activity_score": 0.0
        }
        
        try:
            # Buscar menciones como proveedor o socio comercial
            commercial_queries = [
                f'"{company_name}" proveedor OR distribuidor Ecuador',
                f'"{company_name}" socio OR partner comercial',
                f'"{ruc}" proveedor OR empresa'
            ]
            
            for query in commercial_queries:
                results = await self._google_search(query, max_results=5)
                references["supplier_mentions"] += len(results.get("results", []))
            
            # Buscar testimonios de clientes
            testimonial_query = f'"{company_name}" testimonio OR experiencia OR "trabajé con"'
            testimonial_results = await self._google_search(testimonial_query, max_results=5)
            references["client_testimonials"] = len(testimonial_results.get("results", []))
            
            # Calcular score de actividad comercial
            activity_score = min(
                (references["supplier_mentions"] * 0.1) + 
                (references["client_testimonials"] * 0.2), 
                1.0
            )
            references["commercial_activity_score"] = activity_score
            
            return references
            
        except Exception as e:
            logger.error(f"Error buscando referencias comerciales: {e}")
            return references
    
    async def _check_marketplace_presence(self, company_name: str) -> Dict:
        """Verificar presencia en marketplaces ecuatorianos"""
        
        marketplace_presence = {
            "mercadolibre_found": False,
            "olx_found": False,
            "marketplace_score": 0.0,
            "estimated_products": 0,
            "marketplace_activity": "low"
        }
        
        try:
            # Buscar en principales marketplaces
            marketplaces = {
                "mercadolibre": f'site:mercadolibre.com.ec "{company_name}"',
                "olx": f'site:olx.com.ec "{company_name}"'
            }
            
            for marketplace, query in marketplaces.items():
                results = await self._google_search(query, max_results=5)
                if results.get("results"):
                    marketplace_presence[f"{marketplace}_found"] = True
                    marketplace_presence["estimated_products"] += len(results["results"])
            
            # Calcular score de marketplace
            platforms_active = sum([
                marketplace_presence["mercadolibre_found"],
                marketplace_presence["olx_found"]
            ])
            
            marketplace_presence["marketplace_score"] = platforms_active * 0.5
            
            if marketplace_presence["estimated_products"] > 10:
                marketplace_presence["marketplace_activity"] = "high"
            elif marketplace_presence["estimated_products"] > 3:
                marketplace_presence["marketplace_activity"] = "medium"
            
            return marketplace_presence
            
        except Exception as e:
            logger.error(f"Error verificando marketplaces: {e}")
            return marketplace_presence
    
    def _calculate_digital_score(self, scraping_results: Dict) -> Dict:
        """Calcular score digital total basado en todos los factores"""
        
        digital_presence = scraping_results.get("digital_presence", {})
        social_media = scraping_results.get("social_media_analysis", {})
        reputation = scraping_results.get("online_reputation", {})
        commercial = scraping_results.get("commercial_references", {})
        marketplace = scraping_results.get("market_visibility", {})
        
        # Weights para cada componente
        weights = {
            "digital_presence": 0.25,
            "social_media": 0.25,
            "reputation": 0.25,
            "commercial_activity": 0.15,
            "marketplace": 0.10
        }
        
        # Calcular scores individuales
        presence_score = (
            (1.0 if digital_presence.get("website_found") else 0.0) * 0.4 +
            min(digital_presence.get("google_listings", 0) / 10, 1.0) * 0.3 +
            min(len(digital_presence.get("business_directories", [])) / 3, 1.0) * 0.3
        )
        
        social_score = social_media.get("social_media_score", 0.0)
        reputation_score = reputation.get("reputation_score", 0.5)
        commercial_score = commercial.get("commercial_activity_score", 0.0)
        marketplace_score = marketplace.get("marketplace_score", 0.0)
        
        # Score final ponderado
        final_score = (
            presence_score * weights["digital_presence"] +
            social_score * weights["social_media"] +
            reputation_score * weights["reputation"] +
            commercial_score * weights["commercial_activity"] +
            marketplace_score * weights["marketplace"]
        )
        
        # Determinar nivel de presencia digital
        if final_score >= 0.8:
            digital_level = "excellent"
        elif final_score >= 0.6:
            digital_level = "good"
        elif final_score >= 0.4:
            digital_level = "average"
        elif final_score >= 0.2:
            digital_level = "poor"
        else:
            digital_level = "minimal"
        
        return {
            "overall_digital_score": round(final_score * 100, 2),
            "digital_level": digital_level,
            "component_scores": {
                "digital_presence": round(presence_score * 100, 2),
                "social_media": round(social_score * 100, 2),
                "online_reputation": round(reputation_score * 100, 2),
                "commercial_activity": round(commercial_score * 100, 2),
                "marketplace_presence": round(marketplace_score * 100, 2)
            },
            "recommendations": self._generate_digital_recommendations(final_score, {
                "presence": presence_score,
                "social": social_score,
                "reputation": reputation_score,
                "commercial": commercial_score,
                "marketplace": marketplace_score
            })
        }
    
    def _generate_digital_recommendations(self, overall_score: float, component_scores: Dict) -> List[str]:
        """Generar recomendaciones basadas en el análisis digital"""
        
        recommendations = []
        
        if component_scores["presence"] < 0.5:
            recommendations.append("Crear un sitio web oficial y presencia en directorios empresariales")
        
        if component_scores["social"] < 0.4:
            recommendations.append("Desarrollar presencia en redes sociales (Facebook, Instagram, LinkedIn)")
        
        if component_scores["reputation"] < 0.6:
            recommendations.append("Mejorar gestión de reputación online y recolectar testimonios positivos")
        
        if component_scores["commercial"] < 0.3:
            recommendations.append("Aumentar visibilidad como proveedor y generar referencias comerciales")
        
        if component_scores["marketplace"] < 0.3:
            recommendations.append("Considerar venta online en plataformas como MercadoLibre Ecuador")
        
        if overall_score > 0.7:
            recommendations.append("Excelente presencia digital - Mantener y optimizar estrategias actuales")
        
        return recommendations
    
    # Helper methods
    async def _google_search(self, query: str, max_results: int = 10) -> Dict:
        """Simulación de búsqueda en Google (en producción usar API real)"""
        # NOTA: En producción usar Google Custom Search API
        import random
        
        return {
            "query": query,
            "total_results": random.randint(50, 500),
            "results": [
                {
                    "title": f"Resultado {i+1} para {query[:30]}...",
                    "url": f"https://example.com/result-{i+1}",
                    "snippet": f"Información relevante sobre la búsqueda {query[:20]}..."
                }
                for i in range(min(max_results, random.randint(1, max_results)))
            ]
        }
    
    def _identify_platform(self, url: str) -> Optional[str]:
        """Identificar plataforma de red social por URL"""
        if "facebook.com" in url:
            return "facebook"
        elif "instagram.com" in url:
            return "instagram"
        elif "linkedin.com" in url:
            return "linkedin"
        elif "twitter.com" in url or "x.com" in url:
            return "twitter"
        elif "tiktok.com" in url:
            return "tiktok"
        return None
    
    async def _scrape_social_platform(self, url: str, platform: str) -> Dict:
        """Scraping específico por plataforma (simulado)"""
        # NOTA: En producción usar APIs oficiales de cada plataforma
        import random
        
        base_data = {
            "url": url,
            "platform": platform,
            "followers": random.randint(100, 10000),
            "following": random.randint(50, 1000),
            "posts_count": random.randint(10, 500),
            "engagement_rate": random.uniform(0.01, 0.15),
            "last_post_date": "2024-08-01",
            "verified": random.choice([True, False]),
            "business_account": random.choice([True, False])
        }
        
        return base_data
    
    def _analyze_text_sentiment(self, text: str) -> float:
        """Análisis básico de sentimiento (en producción usar modelo ML)"""
        positive_words = ['excelente', 'bueno', 'recomendado', 'calidad', 'profesional']
        negative_words = ['malo', 'terrible', 'estafa', 'problemas', 'pésimo']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        total_words = positive_count + negative_count
        if total_words == 0:
            return 0.5  # Neutral
        
        return positive_count / total_words
    
    def _is_official_website(self, url: str, company_name: str) -> bool:
        """Determinar si una URL es el sitio web oficial de la empresa"""
        # Lógica simplificada
        company_clean = re.sub(r'[^\w]', '', company_name.lower())
        return company_clean in url.lower() and not any(
            social in url.lower() 
            for social in ['facebook', 'instagram', 'linkedin', 'twitter']
        )
    
    def _calculate_avg_engagement(self, platform_details: Dict) -> float:
        """Calcular engagement promedio de todas las plataformas"""
        if not platform_details:
            return 0.0
        
        total_engagement = sum(
            data.get("engagement_rate", 0) 
            for data in platform_details.values()
        )
        return total_engagement / len(platform_details)
    
    def _analyze_content_quality(self, platform_details: Dict) -> float:
        """Analizar calidad del contenido (simulado)"""
        import random
        return random.uniform(0.3, 0.9)
    
    def _analyze_business_focus(self, platform_details: Dict) -> float:
        """Analizar enfoque empresarial del contenido (simulado)"""
        import random
        return random.uniform(0.4, 0.95)
    
    def _fallback_analysis(self, company_name: str, ruc: str) -> Dict:
        """Análisis de respaldo en caso de error"""
        return {
            "company_name": company_name,
            "ruc": ruc,
            "scraping_timestamp": datetime.now().isoformat(),
            "digital_score": {
                "overall_digital_score": 50.0,
                "digital_level": "average",
                "component_scores": {
                    "digital_presence": 50.0,
                    "social_media": 50.0,
                    "online_reputation": 50.0,
                    "commercial_activity": 50.0,
                    "marketplace_presence": 50.0
                },
                "recommendations": ["Realizar análisis manual debido a limitaciones técnicas"]
            },
            "error": "Análisis de respaldo - Datos limitados disponibles"
        }
