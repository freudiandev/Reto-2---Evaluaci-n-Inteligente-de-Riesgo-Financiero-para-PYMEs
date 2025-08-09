# Sistema de Evaluación de Riesgo Financiero para PYMEs

Sistema web para evaluar el riesgo crediticio de pequeñas y medianas empresas en Ecuador.

## Qué hace

- Calcula el riesgo financiero de empresas que solicitan créditos
- Analiza documentos financieros subidos por las empresas
- Muestra estadísticas y gráficos del estado de las solicitudes
- Permite simular diferentes escenarios de riesgo

## Cómo funciona

El sistema tiene dos partes principales:

**Backend (Python)**: Procesa la información, calcula los riesgos y maneja la base de datos. Está desplegado en Render.

**Frontend (React)**: La interfaz donde los usuarios ven la información y suben documentos. Se puede desplegar en Vercel.

## Para ejecutar localmente

### Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Para producción

- Backend: Ya está en https://backend-riesgo-pymes-the-orellanas-boyz.onrender.com
- Frontend: Se puede subir a Vercel con `npm run build`

## Tecnologías

- Python con FastAPI
- React con TypeScript
- Base de datos SQLite
- CSS responsive para móviles y desktop

## Estructura

- `/backend` - API y lógica de negocio
- `/frontend` - Interfaz de usuario
- `/database` - Archivos de base de datos
- `docker-compose.yml` - Para ejecutar con Docker

El sistema funciona bien para evaluar riesgos básicos de PYMEs ecuatorianas.
