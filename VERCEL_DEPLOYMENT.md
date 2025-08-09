# Despliegue del Frontend en Vercel

## Pasos para desplegar en Vercel:

### 1. Ir a Vercel
- Visita: https://vercel.com
- Inicia sesión con tu cuenta de GitHub

### 2. Importar proyecto
- Clic en "New Project"
- Busca tu repositorio: `Reto-2---Evaluaci-n-Inteligente-de-Riesgo-Financiero-para-PYMEs`
- Clic en "Import"

### 3. Configuración del proyecto
```
Project Name: pymes-risk-frontend
Framework Preset: Vite
Root Directory: frontend
Build Command: npm run build
Output Directory: dist
Install Command: npm install
```

### 4. Variables de entorno
Agregar estas variables en Vercel:
```
VITE_API_URL=https://backend-riesgo-pymes-the-orellanas-boyz.onrender.com
```

### 5. Deploy
- Clic en "Deploy"
- Esperar a que termine el despliegue

## Después del despliegue:

1. Obtendrás una URL como: `https://pymes-risk-frontend.vercel.app`
2. Actualizar CORS en Render con esta URL
3. Probar la aplicación completa

## Troubleshooting:
- Si hay errores de build, verificar package.json
- Si hay errores de CORS, verificar configuración del backend
