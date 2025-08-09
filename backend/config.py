# Configuración de la base de datos
DATABASE_URL = "sqlite:///./database/pymes_risk.db"

# Configuración de la API
API_HOST = "0.0.0.0"
API_PORT = 8000

# Configuración de archivos
UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Configuración de web scraping
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
REQUEST_TIMEOUT = 30

# Configuración del modelo de IA
MODEL_VERSION = "1.0"
RISK_THRESHOLDS = {
    "low": 0.7,
    "medium": 0.4,
    "high": 0.0
}

# Sectores económicos de Ecuador
ECUADOR_SECTORS = [
    "Agricultura, ganadería, silvicultura y pesca",
    "Explotación de minas y canteras",
    "Industrias manufactureras",
    "Suministro de electricidad, gas, vapor",
    "Distribución de agua; alcantarillado",
    "Construcción",
    "Comercio al por mayor y al por menor",
    "Transporte y almacenamiento",
    "Actividades de alojamiento y de servicio de comidas",
    "Información y comunicación",
    "Actividades financieras y de seguros",
    "Actividades inmobiliarias",
    "Actividades profesionales, científicas y técnicas",
    "Actividades de servicios administrativos",
    "Administración pública y defensa",
    "Enseñanza",
    "Actividades de atención de la salud humana",
    "Artes, entretenimiento y recreación",
    "Otras actividades de servicios",
    "Actividades de los hogares"
]

# Configuración de logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
