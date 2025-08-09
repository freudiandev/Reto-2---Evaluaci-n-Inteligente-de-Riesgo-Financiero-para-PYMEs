#!/bin/bash

echo "🔄 Post-Deployment URL Update Script"
echo "====================================="
echo

# Solicitar URLs del usuario
echo "📝 Por favor ingresa las URLs obtenidas después del deployment:"
echo

read -p "🚂 URL de Railway (Backend): " RAILWAY_URL
read -p "▲ URL de Vercel (Frontend): " VERCEL_URL

echo
echo "🔄 Actualizando archivos de configuración..."

# Actualizar archivo de variables de Vercel
cat > VERCEL_VARIABLES_UPDATED.txt << EOF
# 🔧 VARIABLES ACTUALIZADAS PARA VERCEL

VITE_API_URL=${RAILWAY_URL}/api/v1
VITE_BACKEND_URL=${RAILWAY_URL}
NODE_ENV=production
EOF

# Actualizar archivo de variables de Railway
cat > RAILWAY_VARIABLES_UPDATED.txt << EOF
# 🔧 VARIABLES ACTUALIZADAS PARA RAILWAY

PORT=8000
DATABASE_URL=sqlite:///./database/app.db
SECRET_KEY=EkJa9SGw5qSByKzz9cpwMqe^NA0xt1HusErA*YGpX$y%Igj%loqO1cTKttvFeqST
ENVIRONMENT=production
DEBUG=false
API_V1_STR=/api/v1
PROJECT_NAME=PyMEs Risk Assessment
CORS_ORIGINS=${VERCEL_URL}
EOF

# Actualizar archivo .env.production del frontend
cat > frontend/.env.production << EOF
VITE_API_URL=${RAILWAY_URL}/api/v1
VITE_BACKEND_URL=${RAILWAY_URL}
NODE_ENV=production
EOF

echo "✅ Archivos actualizados:"
echo "   - VERCEL_VARIABLES_UPDATED.txt"
echo "   - RAILWAY_VARIABLES_UPDATED.txt"
echo "   - frontend/.env.production"
echo
echo "📋 Próximos pasos:"
echo "1. Ve a Vercel → Settings → Environment Variables"
echo "2. Actualiza con las variables de VERCEL_VARIABLES_UPDATED.txt"
echo "3. Ve a Railway → Variables"
echo "4. Actualiza CORS_ORIGINS con: ${VERCEL_URL}"
echo "5. Redeploy ambos servicios"
echo
echo "🎉 URLs finales:"
echo "   Frontend: ${VERCEL_URL}"
echo "   Backend:  ${RAILWAY_URL}"
echo "   API Docs: ${RAILWAY_URL}/docs"
echo "   Health:   ${RAILWAY_URL}/api/v1/health"
