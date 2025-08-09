@echo off
echo 🔄 Post-Deployment URL Update Script
echo =====================================
echo.

REM Solicitar URLs del usuario
echo 📝 Por favor ingresa las URLs obtenidas después del deployment:
echo.

set /p RAILWAY_URL="🚂 URL de Railway (Backend): "
set /p VERCEL_URL="▲ URL de Vercel (Frontend): "

echo.
echo 🔄 Actualizando archivos de configuración...

REM Actualizar archivo de variables de Vercel
echo # 🔧 VARIABLES ACTUALIZADAS PARA VERCEL > VERCEL_VARIABLES_UPDATED.txt
echo. >> VERCEL_VARIABLES_UPDATED.txt
echo VITE_API_URL=%RAILWAY_URL%/api/v1 >> VERCEL_VARIABLES_UPDATED.txt
echo VITE_BACKEND_URL=%RAILWAY_URL% >> VERCEL_VARIABLES_UPDATED.txt
echo NODE_ENV=production >> VERCEL_VARIABLES_UPDATED.txt

REM Actualizar archivo de variables de Railway
echo # 🔧 VARIABLES ACTUALIZADAS PARA RAILWAY > RAILWAY_VARIABLES_UPDATED.txt
echo. >> RAILWAY_VARIABLES_UPDATED.txt
echo PORT=8000 >> RAILWAY_VARIABLES_UPDATED.txt
echo DATABASE_URL=sqlite:///./database/app.db >> RAILWAY_VARIABLES_UPDATED.txt
echo SECRET_KEY=EkJa9SGw5qSByKzz9cpwMqe^NA0xt1HusErA*YGpX$y%Igj%loqO1cTKttvFeqST >> RAILWAY_VARIABLES_UPDATED.txt
echo ENVIRONMENT=production >> RAILWAY_VARIABLES_UPDATED.txt
echo DEBUG=false >> RAILWAY_VARIABLES_UPDATED.txt
echo API_V1_STR=/api/v1 >> RAILWAY_VARIABLES_UPDATED.txt
echo PROJECT_NAME=PyMEs Risk Assessment >> RAILWAY_VARIABLES_UPDATED.txt
echo CORS_ORIGINS=%VERCEL_URL% >> RAILWAY_VARIABLES_UPDATED.txt

REM Actualizar archivo .env.production del frontend
echo VITE_API_URL=%RAILWAY_URL%/api/v1 > frontend\.env.production
echo VITE_BACKEND_URL=%RAILWAY_URL% >> frontend\.env.production
echo NODE_ENV=production >> frontend\.env.production

echo ✅ Archivos actualizados:
echo    - VERCEL_VARIABLES_UPDATED.txt
echo    - RAILWAY_VARIABLES_UPDATED.txt
echo    - frontend\.env.production
echo.
echo 📋 Próximos pasos:
echo 1. Ve a Vercel → Settings → Environment Variables
echo 2. Actualiza con las variables de VERCEL_VARIABLES_UPDATED.txt
echo 3. Ve a Railway → Variables
echo 4. Actualiza CORS_ORIGINS con: %VERCEL_URL%
echo 5. Redeploy ambos servicios
echo.
echo 🎉 URLs finales:
echo    Frontend: %VERCEL_URL%
echo    Backend:  %RAILWAY_URL%
echo    API Docs: %RAILWAY_URL%/docs
echo    Health:   %RAILWAY_URL%/api/v1/health
echo.
pause
