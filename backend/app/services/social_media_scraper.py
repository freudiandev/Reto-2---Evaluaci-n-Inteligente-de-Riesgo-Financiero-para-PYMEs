import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Dict, List, Optional
import json
import time
import re
from urllib.parse import urlparse
from config import USER_AGENT, REQUEST_TIMEOUT

class SocialMediaScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': USER_AGENT})
        
        # Configurar Selenium para casos que requieran JavaScript
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument(f'--user-agent={USER_AGENT}')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
        except:
            self.driver = None
            print("Warning: Chrome driver not available. Some features may be limited.")

    def analyze_facebook_page(self, url: str) -> Dict:
        """Analizar página de Facebook"""
        try:
            # Facebook requiere métodos más sofisticados debido a sus restricciones
            # Simulamos datos por ahora
            return self._simulate_facebook_data(url)
        except Exception as e:
            print(f"Error analizando Facebook: {e}")
            return {}

    def analyze_instagram_profile(self, url: str) -> Dict:
        """Analizar perfil de Instagram"""
        try:
            if self.driver:
                self.driver.get(url)
                time.sleep(3)
                
                # Extraer información básica
                data = {}
                
                try:
                    # Número de publicaciones, seguidores, siguiendo
                    stats = self.driver.find_elements(By.CSS_SELECTOR, "span._ac2a")
                    if len(stats) >= 3:
                        data['posts_count'] = self._extract_number(stats[0].text)
                        data['followers_count'] = self._extract_number(stats[1].text)
                        data['following_count'] = self._extract_number(stats[2].text)
                    
                    # Descripción/Bio
                    bio = self.driver.find_element(By.CSS_SELECTOR, "div._aa_c")
                    data['bio'] = bio.text if bio else ""
                    
                    # Verificar si es cuenta de negocio
                    data['is_business'] = self._check_business_account()
                    
                except Exception as e:
                    print(f"Error extrayendo datos de Instagram: {e}")
                
                return data
            else:
                return self._simulate_instagram_data(url)
                
        except Exception as e:
            print(f"Error analizando Instagram: {e}")
            return {}

    def analyze_linkedin_page(self, url: str) -> Dict:
        """Analizar página de LinkedIn"""
        try:
            response = self.session.get(url, timeout=REQUEST_TIMEOUT)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            data = {}
            
            # Nombre de la empresa
            name_tag = soup.find('h1', {'class': 'org-top-card-summary__title'})
            if name_tag:
                data['company_name'] = name_tag.text.strip()
            
            # Número de empleados
            employees_tag = soup.find('dd', {'class': 'org-top-card-summary__info-item'})
            if employees_tag:
                data['employees_text'] = employees_tag.text.strip()
                data['employees_count'] = self._extract_employee_count(employees_tag.text)
            
            # Sector/Industria
            industry_tag = soup.find('div', {'class': 'org-top-card-summary__info-item'})
            if industry_tag:
                data['industry'] = industry_tag.text.strip()
            
            # Descripción
            desc_tag = soup.find('p', {'class': 'break-words'})
            if desc_tag:
                data['description'] = desc_tag.text.strip()
            
            return data
            
        except Exception as e:
            print(f"Error analizando LinkedIn: {e}")
            return self._simulate_linkedin_data(url)

    def analyze_twitter_profile(self, url: str) -> Dict:
        """Analizar perfil de Twitter"""
        try:
            # Twitter/X tiene fuertes restricciones, simulamos datos
            return self._simulate_twitter_data(url)
        except Exception as e:
            print(f"Error analizando Twitter: {e}")
            return {}

    def get_platform_from_url(self, url: str) -> str:
        """Identificar la plataforma desde la URL"""
        domain = urlparse(url).netloc.lower()
        
        if 'facebook.com' in domain:
            return 'facebook'
        elif 'instagram.com' in domain:
            return 'instagram'
        elif 'linkedin.com' in domain:
            return 'linkedin'
        elif 'twitter.com' in domain or 'x.com' in domain:
            return 'twitter'
        elif 'tiktok.com' in domain:
            return 'tiktok'
        else:
            return 'unknown'

    def analyze_social_media(self, url: str) -> Dict:
        """Método principal para analizar cualquier red social"""
        platform = self.get_platform_from_url(url)
        
        analyzers = {
            'facebook': self.analyze_facebook_page,
            'instagram': self.analyze_instagram_profile,
            'linkedin': self.analyze_linkedin_page,
            'twitter': self.analyze_twitter_profile,
        }
        
        if platform in analyzers:
            data = analyzers[platform](url)
            data['platform'] = platform
            data['url'] = url
            return data
        else:
            return {'platform': 'unknown', 'url': url, 'error': 'Platform not supported'}

    def _extract_number(self, text: str) -> int:
        """Extraer número de texto (maneja K, M, etc.)"""
        text = text.replace(',', '').replace('.', '')
        multipliers = {'K': 1000, 'M': 1000000, 'B': 1000000000}
        
        for suffix, multiplier in multipliers.items():
            if suffix in text.upper():
                number = float(re.findall(r'[\d.]+', text)[0])
                return int(number * multiplier)
        
        numbers = re.findall(r'\d+', text)
        return int(numbers[0]) if numbers else 0

    def _extract_employee_count(self, text: str) -> int:
        """Extraer número de empleados de texto de LinkedIn"""
        if '1-10' in text:
            return 5
        elif '11-50' in text:
            return 30
        elif '51-200' in text:
            return 125
        elif '201-500' in text:
            return 350
        elif '501-1000' in text:
            return 750
        elif '1001-5000' in text:
            return 3000
        elif '5001-10000' in text:
            return 7500
        else:
            return self._extract_number(text)

    def _check_business_account(self) -> bool:
        """Verificar si es cuenta de negocio en Instagram"""
        try:
            # Buscar indicadores de cuenta de negocio
            business_indicators = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='business_category']")
            return len(business_indicators) > 0
        except:
            return False

    # Métodos de simulación para cuando el scraping real no esté disponible
    def _simulate_facebook_data(self, url: str) -> Dict:
        return {
            'platform': 'facebook',
            'url': url,
            'followers_count': 1250,
            'posts_count': 45,
            'page_likes': 1100,
            'reviews_count': 23,
            'average_rating': 4.2,
            'last_post_date': '2024-08-05',
            'posting_frequency': 'weekly',
            'business_verified': True,
            'simulated': True
        }

    def _simulate_instagram_data(self, url: str) -> Dict:
        return {
            'platform': 'instagram',
            'url': url,
            'followers_count': 850,
            'following_count': 120,
            'posts_count': 67,
            'is_business': True,
            'engagement_rate': 3.2,
            'last_post_date': '2024-08-07',
            'posting_frequency': 'daily',
            'bio': 'Empresa ecuatoriana dedicada a soluciones innovadoras',
            'simulated': True
        }

    def _simulate_linkedin_data(self, url: str) -> Dict:
        return {
            'platform': 'linkedin',
            'url': url,
            'company_name': 'Empresa PYME Ecuador',
            'employees_count': 25,
            'followers_count': 340,
            'industry': 'Tecnología y servicios',
            'description': 'Empresa dedicada a brindar soluciones tecnológicas',
            'established_year': 2018,
            'simulated': True
        }

    def _simulate_twitter_data(self, url: str) -> Dict:
        return {
            'platform': 'twitter',
            'url': url,
            'followers_count': 450,
            'following_count': 180,
            'tweets_count': 234,
            'likes_count': 1240,
            'verified': False,
            'last_tweet_date': '2024-08-06',
            'posting_frequency': 'weekly',
            'simulated': True
        }

    def __del__(self):
        """Cerrar el driver de Selenium"""
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()
