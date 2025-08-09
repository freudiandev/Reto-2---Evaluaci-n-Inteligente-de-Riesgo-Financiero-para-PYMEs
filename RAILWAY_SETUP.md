# 🔧 Variables de Entorno para Railway

## 📋 Configuración del Backend en Railway

Copia y pega estas variables en la configuración de Railway:

```bash
# Configuración principal
PORT=8000
DATABASE_URL=sqlite:///./database/app.db
SECRET_KEY=EkJa9SGw5qSByKzz9cpwMqe^NA0xt1HusErA*YGpX$y%Igj%loqO1cTKttvFeqST
ENVIRONMENT=production

# CORS - Actualizar con la URL real del frontend
CORS_ORIGINS=https://tu-proyecto.vercel.app

# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=PyMEs Risk Assessment
DEBUG=false

# Database settings (si usas PostgreSQL en Railway)
# DATABASE_URL=postgresql://user:password@hostname:port/database_name
```

## 🔧 Variables de Entorno para Vercel (Frontend)

```bash
# API Configuration
VITE_API_URL=https://tu-proyecto.railway.app/api/v1
VITE_BACKEND_URL=https://tu-proyecto.railway.app
NODE_ENV=production
```

## 📝 Pasos para Railway:

1. Ve a [railway.app](https://railway.app)
2. Conecta tu cuenta de GitHub
3. Selecciona "Deploy from GitHub repo"
4. Autoriza Railway y selecciona tu repositorio
5. Railway detectará automáticamente el `Dockerfile`
6. Ve a Variables → Añade las variables de arriba
7. Clic en "Deploy"

## 📝 Pasos para Vercel:

1. Ve a [vercel.com](https://vercel.com)
2. Importa tu repositorio de GitHub
3. Configuración del proyecto:
   - **Framework Preset**: Vite
   - **Root Directory**: frontend
   - **Build Command**: npm run build
   - **Output Directory**: dist
4. Ve a Settings → Environment Variables
5. Añade las variables del frontend
6. Redeploy

## 🔄 Actualizar URLs después del deployment:

1. **Después de deployar el backend en Railway**:
   - Copia la URL generada (ej: `https://tu-proyecto.railway.app`)
   - Actualiza `VITE_API_URL` y `VITE_BACKEND_URL` en Vercel
   - Redeploy el frontend

2. **Después de deployar el frontend en Vercel**:
   - Copia la URL generada (ej: `https://tu-proyecto.vercel.app`)
   - Actualiza `CORS_ORIGINS` en Railway
   - Redeploy el backend

## ✅ URLs finales:

- **Frontend**: `https://tu-proyecto.vercel.app`
- **Backend**: `https://tu-proyecto.railway.app`
- **API Docs**: `https://tu-proyecto.railway.app/docs`
- **Health Check**: `https://tu-proyecto.railway.app/api/v1/health`

## 🚨 Troubleshooting:

### Error de CORS
Si el frontend no puede conectar al backend:
1. Verifica que `CORS_ORIGINS` en Railway incluya la URL exacta de Vercel
2. Sin trailing slash: `https://tu-proyecto.vercel.app` (no `https://tu-proyecto.vercel.app/`)

### Error 500 en Railway
1. Ve a Railway → tu proyecto → Deployments → View Logs
2. Busca errores específicos
3. Verifica que todas las variables estén configuradas

### Frontend muestra error de conexión
1. Ve a Vercel → tu proyecto → Functions → View Function Logs  
2. Verifica que `VITE_API_URL` sea correcta
3. Prueba la URL del backend directamente en el navegador
