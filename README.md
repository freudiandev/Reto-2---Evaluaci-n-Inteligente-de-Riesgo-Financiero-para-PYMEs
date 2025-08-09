# Evaluación Inteligente de Riesgo Financiero para PYMEs

## 🏆 Descripción del Proyecto

Sistema integral de evaluación de riesgo financiero basado en inteligencia artificial para pequeñas y medianas empresas (PYMEs) en Ecuador. El sistema utiliza datos tradicionales y no tradicionales (comportamiento digital, redes sociales, referencias) para democratizar el acceso al crédito.

## 🎯 Objetivos

- **Objetivo Principal**: Crear una solución de IA que evalúe el riesgo financiero de PYMEs usando datos no tradicionales
- **Democratizar el acceso al crédito** para empresas sin historial crediticio formal
- **Agilizar el proceso** de análisis crediticio
- **Reducir el riesgo** de impagos mediante evaluaciones más precisas
- **Identificar negocios saludables** aunque sean informales

## 🚀 Características Principales

### 💡 Inteligencia Artificial
- **Scoring alternativo** basado en múltiples fuentes de datos
- **Análisis de sentimientos** en redes sociales
- **Procesamiento de lenguaje natural** para referencias y comentarios
- **Modelos de machine learning** para evaluación de riesgo
- **Simulaciones de escenarios** financieros

### 📊 Fuentes de Datos
- **Estados financieros** de la Superintendencia de Compañías
- **Redes sociales** (Facebook, Instagram, LinkedIn, Twitter)
- **Referencias comerciales** y reputación online
- **Comportamiento digital** y actividad en plataformas
- **Datos de terceros** y proveedores

### 🎨 Dashboard Interactivo
- **Visualizaciones** de riesgo en tiempo real
- **Comparativo sectorial** y benchmarking
- **Justificación** del scoring con factores principales
- **Simulaciones** "qué pasaría si..."
- **Reportes** exportables en PDF

## 🏗️ Arquitectura del Sistema

### Backend (Python/FastAPI)
```
backend/
├── app/
│   ├── ai/                    # Modelos de IA y ML
│   │   ├── risk_model.py      # Modelo principal de scoring
│   │   └── sentiment_analyzer.py # Análisis de sentimientos
│   ├── api/                   # Endpoints de la API
│   │   └── routes.py
│   ├── models/                # Modelos de datos
│   │   ├── database.py        # Modelos SQLAlchemy
│   │   └── schemas.py         # Esquemas Pydantic
│   └── services/              # Servicios de negocio
│       ├── database.py        # Conexión a BD
│       ├── document_processor.py # Procesamiento de archivos
│       └── social_media_scraper.py # Web scraping
├── main.py                    # Aplicación principal
├── config.py                  # Configuración
└── requirements.txt           # Dependencias
```

### Frontend (React/TypeScript)
```
frontend/
├── src/
│   ├── components/            # Componentes reutilizables
│   │   ├── Layout.tsx         # Layout principal
│   │   ├── StatsCard.tsx      # Tarjetas de estadísticas
│   │   ├── RiskLevelChart.tsx # Gráfico de niveles de riesgo
│   │   └── SectorChart.tsx    # Gráfico de sectores
│   ├── pages/                 # Páginas de la aplicación
│   │   ├── Dashboard.tsx      # Dashboard principal
│   │   ├── Companies.tsx      # Gestión de empresas
│   │   ├── Applications.tsx   # Solicitudes de crédito
│   │   ├── RiskAnalysis.tsx   # Análisis de riesgo
│   │   └── Simulations.tsx    # Simulaciones
│   ├── services/              # Servicios de API
│   │   ├── api.ts             # Cliente HTTP
│   │   └── apiServices.ts     # Servicios específicos
│   ├── types/                 # Tipos TypeScript
│   │   └── index.ts
│   └── hooks/                 # Custom hooks
├── package.json
├── vite.config.ts
└── tailwind.config.js
```

### Base de Datos (SQLite)
```sql
-- Tablas principales:
- companies              # Empresas registradas
- credit_applications    # Solicitudes de crédito
- financial_statements   # Estados financieros
- social_media_analysis  # Análisis de redes sociales
- risk_scores           # Puntuaciones de riesgo
- simulation_scenarios  # Simulaciones de escenarios
```

## 🔧 Tecnologías Utilizadas

### Backend
- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para base de datos
- **Pandas**: Manipulación de datos
- **Scikit-learn**: Machine learning
- **NLTK/TextBlob**: Procesamiento de lenguaje natural
- **BeautifulSoup**: Web scraping
- **Selenium**: Scraping dinámico
- **Requests**: Cliente HTTP

### Frontend
- **React 18**: Biblioteca de UI
- **TypeScript**: Tipado estático
- **Vite**: Build tool rápido
- **Tailwind CSS**: Framework de CSS
- **React Router**: Navegación
- **Axios**: Cliente HTTP
- **React Hook Form**: Manejo de formularios
- **Chart.js**: Visualizaciones

### IA y ML
- **Random Forest**: Clasificación de riesgo
- **Gradient Boosting**: Regresión de scoring
- **VADER Sentiment**: Análisis de sentimientos
- **Standard Scaler**: Normalización de datos
- **Feature Engineering**: Extracción de características

## 📊 Modelo de IA

### Características del Modelo
```python
# Características financieras (50% peso)
- Ratio de liquidez corriente
- Ratio de endeudamiento
- Retorno sobre activos (ROA)
- Retorno sobre patrimonio (ROE)
- Margen de utilidad
- Rotación de activos
- Crecimiento de ingresos
- Ratio de flujo de caja

# Características de redes sociales (25% peso)
- Número de seguidores
- Número de publicaciones
- Tasa de engagement
- Puntuación de sentimiento
- Calidad del contenido profesional
- Frecuencia de publicación

# Características del negocio (25% peso)
- Años en el mercado
- Puntuación de riesgo sectorial
- Número de empleados
- Presencia web
- Presencia en redes sociales
- Verificación de negocio
```

### Niveles de Riesgo
- **Bajo (70-100 puntos)**: Crédito preferencial, tasas bajas
- **Medio (40-69 puntos)**: Crédito estándar, garantías moderadas
- **Alto (0-39 puntos)**: Requiere análisis detallado, garantías robustas

## 🎨 Funcionalidades Principales

### 1. Gestión de Empresas
- Registro de empresas con RUC ecuatoriano
- Integración con datos de Superintendencia de Compañías
- Validación automática de información

### 2. Procesamiento de Estados Financieros
- Carga de archivos Excel, PDF, Word
- Extracción automática de datos financieros
- Cálculo de ratios financieros clave
- Validación de coherencia contable

### 3. Análisis de Redes Sociales
- Scraping de Facebook, Instagram, LinkedIn, Twitter
- Análisis de sentimientos en publicaciones
- Evaluación de calidad del contenido
- Métricas de engagement y reputación

### 4. Scoring de Riesgo
- Modelo de IA multi-factorial
- Puntuación 0-100 con nivel de riesgo
- Factores de decisión explicados
- Recomendaciones de crédito personalizadas

### 5. Simulaciones Financieras
- Escenarios "qué pasaría si..."
- Impacto de mejoras en ventas/reputación
- Predicción de cambios en scoring
- Planificación financiera

### 6. Dashboard y Reportes
- Resumen ejecutivo de todas las solicitudes
- Distribución por sectores y niveles de riesgo
- Estadísticas de aprobación/rechazo
- Reportes exportables en PDF

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.8+
- Node.js 16+
- npm o yarn

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Variables de Entorno
```bash
# Backend (.env)
DATABASE_URL=sqlite:///./database/pymes_risk.db
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=development

# Frontend (.env)
VITE_API_URL=http://localhost:8000/api/v1
```

## 🌐 Endpoints de la API

### Empresas
- `GET /api/v1/companies/` - Listar empresas
- `POST /api/v1/companies/` - Crear empresa
- `GET /api/v1/companies/{id}` - Obtener empresa
- `GET /api/v1/companies/ruc/{ruc}` - Buscar por RUC

### Solicitudes de Crédito
- `GET /api/v1/applications/` - Listar solicitudes
- `POST /api/v1/applications/` - Crear solicitud
- `GET /api/v1/applications/{id}` - Obtener solicitud

### Estados Financieros
- `POST /api/v1/financial-statements/upload` - Subir archivo
- `POST /api/v1/financial-statements/` - Crear manual

### Análisis de Redes Sociales
- `POST /api/v1/social-media/analyze` - Analizar red social
- `GET /api/v1/social-media/application/{id}` - Obtener análisis

### Scoring de Riesgo
- `POST /api/v1/risk-score/calculate/{application_id}` - Calcular score
- `GET /api/v1/risk-score/application/{id}` - Obtener score

### Simulaciones
- `POST /api/v1/simulations/` - Crear simulación
- `GET /api/v1/simulations/application/{id}` - Obtener simulaciones

### Dashboard
- `GET /api/v1/dashboard/summary` - Resumen general
- `GET /api/v1/reports/risk-analysis/{id}` - Reporte completo

## 🎯 Casos de Uso

### 1. Evaluación Rápida de PYME
```
1. Registro de empresa con RUC
2. Carga de estado financiero
3. Análisis de redes sociales
4. Cálculo automático de score
5. Recomendación de crédito
```

### 2. Análisis Comparativo
```
1. Evaluación de múltiples PYMEs
2. Comparación sectorial
3. Benchmarking de ratios
4. Ranking de riesgo
```

### 3. Simulación de Mejoras
```
1. Score actual de la empresa
2. Simulación de escenarios
3. Impacto de mejoras
4. Plan de acción recomendado
```

## 📈 Impacto Esperado

### Para las PYMEs
- ✅ Mayor acceso al crédito
- ✅ Evaluaciones más justas
- ✅ Procesos más rápidos
- ✅ Orientación para mejoras

### Para las Instituciones Financieras
- ✅ Mejor gestión de riesgo
- ✅ Decisiones más objetivas
- ✅ Reducción de impagos
- ✅ Nuevos mercados

### Para el Ecosistema
- ✅ Inclusión financiera
- ✅ Crecimiento de PYMEs
- ✅ Innovación tecnológica
- ✅ Desarrollo económico

## 🔮 Roadmap Futuro

### Versión 2.0
- [ ] Integración con bancos y cooperativas
- [ ] API del Banco Central del Ecuador
- [ ] Análisis de geolocalización
- [ ] Machine learning avanzado
- [ ] Mobile app

### Versión 3.0
- [ ] Blockchain para trazabilidad
- [ ] IA explicable (XAI)
- [ ] Análisis predictivo
- [ ] Marketplace financiero
- [ ] Expansión regional

## 🤝 Contribución

Este proyecto está diseñado para demostrar capacidades de desarrollo full-stack con IA. Para contribuir:

1. Fork el repositorio
2. Crea una rama feature
3. Implementa mejoras
4. Añade tests
5. Envía pull request

## 📄 Licencia

MIT License - Ver archivo LICENSE para detalles.

## 👥 Equipo

Desarrollado como solución completa para el Reto 2 de Viamatica - Evaluación Inteligente de Riesgo Financiero para PYMEs.

---

**¡Democratizando el acceso al crédito a través de la inteligencia artificial! 🚀**Reto-2---Evaluaci-n-Inteligente-de-Riesgo-Financiero-para-PYMEs
# 🏦 PyMEs Risk Assessment - Sistema de Evaluación de Riesgo Financiero

> **Sistema inteligente de evaluación de riesgo financiero para Pequeñas y Medianas Empresas (PYMEs) en Ecuador**

## 📋 Descripción

Sistema completo de evaluación de riesgo financiero que utiliza inteligencia artificial y análisis de datos para determinar la viabilidad crediticia de PYMEs ecuatorianas. Incluye análisis de estados financieros, verificación de información pública, y generación de reportes automáticos.

## 🚀 Características Principales

### 📊 **Análisis Financiero Avanzado**
- Evaluación automatizada de estados financieros
- Cálculo de ratios financieros clave
- Análisis de tendencias históricas
- Predicción de solvencia

### 🤖 **Inteligencia Artificial**
- Modelos de Machine Learning para predicción de riesgo
- Análisis de sentimientos en noticias y redes sociales
- Procesamiento de lenguaje natural para documentos
- Detección de anomalías en patrones financieros

### 🌐 **Verificación de Datos Públicos**
- Integración con SRI (Servicio de Rentas Internas)
- Consulta de información de superintendencias
- Verificación de antecedentes crediticios
- Análisis de noticias y menciones públicas

### 📱 **Interfaz de Usuario Moderna**
- Dashboard interactivo con métricas en tiempo real
- Visualizaciones avanzadas con gráficos dinámicos
- Interfaz responsive para móviles y escritorio
- Sistema de notificaciones y alertas

## 🛠 Tecnologías

### **Backend**
- **FastAPI**: Framework web moderno y rápido
- **Python 3.11+**: Lenguaje de programación principal
- **SQLAlchemy**: ORM para base de datos
- **Scikit-learn**: Machine Learning y análisis predictivo
- **Pandas & NumPy**: Análisis y manipulación de datos
- **NLTK & SpaCy**: Procesamiento de lenguaje natural
- **Selenium**: Web scraping automatizado
- **SQLite/PostgreSQL**: Base de datos

### **Frontend**
- **React 18**: Biblioteca de interfaz de usuario
- **TypeScript**: Tipado estático para JavaScript
- **Vite**: Build tool rápido y moderno
- **Tailwind CSS**: Framework de estilos utilitarios
- **Chart.js**: Visualización de datos y gráficos

### **DevOps & Deployment**
- **Docker**: Contenedorización
- **Docker Compose**: Orquestación de contenedores
- **Railway/Vercel**: Plataformas de deployment gratuitas
- **GitHub Actions**: CI/CD automatizado

## 🚀 Deployment (¡GRATIS!)

### **Opción 1: Railway + Vercel (Recomendado)**

#### Backend en Railway:
1. Ve a [Railway.app](https://railway.app) y conéctate con GitHub
2. Selecciona este repositorio
3. Railway detectará automáticamente el `Dockerfile`
4. Configura las variables de entorno (ver `.env.production`)

#### Frontend en Vercel:
1. Ve a [Vercel.com](https://vercel.com) e importa el repositorio
2. Configuración:
   - Framework: `Vite`
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`

### **Opción 2: Deployment Local con Docker**

```bash
# Windows
.\deploy-local.bat

# Linux/Mac
chmod +x deploy-local.sh
./deploy-local.sh
```

### **Opción 3: Desarrollo Local**

```bash
# 1. Backend
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python main_simple.py

# 2. Frontend (nueva terminal)
cd frontend
npm install
npm run dev
```

## 📖 Documentación de API

Una vez ejecutándose, la documentación interactiva está disponible en:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🏗 Estructura del Proyecto

```
├── backend/                 # API Backend FastAPI
│   ├── models/             # Modelos de base de datos
│   ├── services/           # Lógica de negocio
│   ├── routers/            # Endpoints de API
│   ├── core/               # Configuración y utilidades
│   ├── main.py             # Aplicación principal
│   ├── main_simple.py      # Versión simplificada para testing
│   └── requirements.txt    # Dependencias Python
├── frontend/               # Interfaz de usuario React
│   ├── src/
│   │   ├── components/     # Componentes React
│   │   ├── pages/          # Páginas de la aplicación
│   │   ├── services/       # Servicios de API
│   │   └── utils/          # Utilidades
│   ├── package.json        # Dependencias Node.js
│   └── Dockerfile          # Contenedor del frontend
├── infra/                  # Infraestructura como código
├── docker-compose.prod.yml # Configuración Docker producción
├── Dockerfile              # Contenedor del backend
└── DEPLOYMENT_GUIDE.md     # Guía completa de deployment
```

## 🔧 Variables de Entorno

### Backend (.env)
```bash
DATABASE_URL=sqlite:///./database/app.db
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=http://localhost:3000,http://localhost:80
ENVIRONMENT=development
API_V1_STR=/api/v1
PROJECT_NAME=PyMEs Risk Assessment
```

### Frontend (.env)
```bash
VITE_API_URL=http://localhost:8000/api/v1
VITE_BACKEND_URL=http://localhost:8000
NODE_ENV=development
```

## 📊 Endpoints Principales

### 🏥 **Health Check**
- `GET /api/v1/health` - Estado del sistema

### 🏢 **Empresas**
- `GET /api/v1/companies/` - Listar empresas
- `POST /api/v1/companies/` - Crear empresa
- `GET /api/v1/companies/{id}` - Obtener empresa
- `PUT /api/v1/companies/{id}` - Actualizar empresa

### 📈 **Evaluaciones**
- `POST /api/v1/evaluations/` - Crear evaluación
- `GET /api/v1/evaluations/{id}` - Obtener evaluación
- `GET /api/v1/evaluations/company/{company_id}` - Evaluaciones por empresa

### 📊 **Dashboard**
- `GET /api/v1/dashboard/summary` - Resumen del dashboard
- `GET /api/v1/dashboard/metrics` - Métricas principales

## 💰 Costos de Deployment

| Plataforma | Costo | Límites |
|------------|-------|---------|
| **Railway** | $5/mes crédito gratis | 500 horas/mes |
| **Vercel** | Gratis | Proyectos ilimitados |
| **Render** | Gratis | 750 horas/mes |
| **Supabase** | Gratis | 500MB base de datos |

## 🚨 Troubleshooting

### Error de CORS
```bash
# Actualizar CORS_ORIGINS en backend/.env
CORS_ORIGINS=https://tu-frontend.vercel.app
```

### Error de Base de Datos
```bash
# Crear directorios necesarios
mkdir -p backend/database backend/uploads backend/logs
```

### Frontend no conecta
```bash
# Verificar variables en frontend/.env
VITE_API_URL=https://tu-backend.railway.app/api/v1
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Soporte

- 📧 **Email**: soporte@pymesrisk.com
- 💬 **Issues**: [GitHub Issues](https://github.com/tu-usuario/pymes-risk/issues)
- 📖 **Documentación**: [Deployment Guide](./DEPLOYMENT_GUIDE.md)

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

---

<div align="center">

**🏦 PyMEs Risk Assessment - Evaluación Inteligente de Riesgo Financiero**

[![Deployment](https://img.shields.io/badge/Deploy-Railway-purple)](https://railway.app)
[![Frontend](https://img.shields.io/badge/Deploy-Vercel-black)](https://vercel.com)
[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://python.org)
[![React](https://img.shields.io/badge/React-18-61dafb)](https://reactjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688)](https://fastapi.tiangolo.com)

</div>
