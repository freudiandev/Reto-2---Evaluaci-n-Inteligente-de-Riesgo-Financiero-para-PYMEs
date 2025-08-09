@echo off
echo 🚀 Iniciando deployment local con Docker...
echo.

REM Verificar que Docker esté ejecutándose
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker no está instalado o no está ejecutándose
    echo 📝 Asegúrate de que Docker Desktop esté ejecutándose
    pause
    exit /b 1
)

echo ✅ Docker está funcionando
echo.

echo 📦 Construyendo imágenes Docker...
docker-compose -f docker-compose.prod.yml build

if %errorlevel% neq 0 (
    echo ❌ Error construyendo las imágenes
    pause
    exit /b 1
)

echo ✅ Imágenes construidas exitosamente
echo.

echo 🚀 Iniciando contenedores...
docker-compose -f docker-compose.prod.yml up -d

if %errorlevel% neq 0 (
    echo ❌ Error iniciando los contenedores
    pause
    exit /b 1
)

echo ✅ Contenedores iniciados exitosamente
echo.
echo 🌐 URLs disponibles:
echo    Frontend: http://localhost:80
echo    Backend:  http://localhost:8000
echo    API Docs: http://localhost:8000/docs
echo.
echo 📝 Para ver los logs: docker-compose -f docker-compose.prod.yml logs -f
echo 📝 Para parar: docker-compose -f docker-compose.prod.yml down
echo.
pause
