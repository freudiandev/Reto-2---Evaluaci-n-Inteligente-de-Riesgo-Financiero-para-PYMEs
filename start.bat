@echo off
chcp 65001 >nul
cls

echo ╔════════════════════════════════════════════════════════════╗
echo ║              🏦 PyMEs Risk Assessment                      ║
echo ║           🚀 INICIO RÁPIDO - DESARROLLO LOCAL              ║
echo ║                     WINDOWS - GRATIS                       ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

echo 💡 Selecciona tu opción de desarrollo GRATUITA:
echo.
echo 1. 🐳 Docker Compose (Recomendado - Simula servidor completo)
echo 2. 🐍 Python Local + Node.js (Simple y rápido)
echo 3. 📱 VS Code Extensions (Más básico)
echo 4. 🌐 GitHub Codespaces (En la nube - 60h gratis/mes)
echo 5. ❌ Salir
echo.
set /p choice="Tu elección (1-5): "

if "%choice%"=="1" goto docker_setup
if "%choice%"=="2" goto local_setup
if "%choice%"=="3" goto vscode_setup
if "%choice%"=="4" goto codespaces_setup
if "%choice%"=="5" goto exit
goto invalid

:docker_setup
echo.
echo 🐳 Configurando con Docker Compose...
echo.

:: Verificar Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker no está instalado.
    echo Instala Docker Desktop desde: https://www.docker.com/products/docker-desktop
    echo Es GRATIS para uso personal.
    pause
    goto end
)

:: Verificar Docker Compose
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose no está instalado.
    echo Viene incluido con Docker Desktop.
    pause
    goto end
)

echo ✅ Docker detectado
echo.
echo 🔨 Construyendo contenedores...
docker-compose -f docker-compose.dev.yml build

echo.
echo 🚀 Levantando servicios...
docker-compose -f docker-compose.dev.yml up -d

echo.
echo 🎉 ¡Servicios iniciados exitosamente!
echo.
echo 📊 URLs disponibles:
echo • Frontend: http://localhost (Nginx proxy)
echo • Backend API: http://localhost:8000
echo • Documentación: http://localhost:8000/docs
echo • Base de datos: http://localhost:8080 (Adminer)
echo • Vite Dev: http://localhost:5173 (directo)
echo.
echo 🔧 Comandos útiles:
echo • Ver logs: docker-compose -f docker-compose.dev.yml logs -f
echo • Detener: docker-compose -f docker-compose.dev.yml down
echo • Reiniciar: docker-compose -f docker-compose.dev.yml restart
echo.
echo Presiona cualquier tecla para abrir el navegador...
pause >nul
start http://localhost
goto end

:local_setup
echo.
echo 🐍 Configurando desarrollo local...
echo.

:: Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado.
    echo Instala Python desde: https://www.python.org/downloads/
    pause
    goto end
)

:: Verificar Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js no está instalado.
    echo Instala Node.js desde: https://nodejs.org/
    pause
    goto end
)

echo ✅ Python y Node.js detectados
echo.

:: Configurar backend
echo 🔨 Configurando backend...
cd backend

:: Crear entorno virtual si no existe
if not exist "venv" (
    echo Creando entorno virtual...
    python -m venv venv
)

:: Activar entorno virtual
echo Activando entorno virtual...
call venv\Scripts\activate.bat

:: Crear directorios
if not exist "database" mkdir database
if not exist "uploads" mkdir uploads
if not exist "logs" mkdir logs

:: Crear archivo .env si no existe
if not exist ".env" (
    echo Creando archivo .env...
    echo DATABASE_URL=sqlite:///./database/pymes_risk.db > .env
    echo API_HOST=0.0.0.0 >> .env
    echo API_PORT=8000 >> .env
    echo ENVIRONMENT=development >> .env
    echo CORS_ORIGINS=http://localhost:3000,http://localhost:5173 >> .env
)

:: Instalar dependencias
echo Instalando dependencias de Python...
pip install --upgrade pip
pip install fastapi uvicorn sqlalchemy sqlite3 pandas scikit-learn nltk textblob python-multipart

cd ..

:: Configurar frontend
echo 🔨 Configurando frontend...
cd frontend

:: Crear archivo .env si no existe
if not exist ".env" (
    echo Creando archivo .env...
    echo VITE_API_URL=http://localhost:8000/api/v1 > .env
    echo VITE_APP_NAME=PyMEs Risk Assessment >> .env
    echo VITE_ENVIRONMENT=development >> .env
)

:: Instalar dependencias si no existen
if not exist "node_modules" (
    echo Instalando dependencias de Node.js...
    npm install
)

cd ..

echo.
echo 🎉 ¡Configuración completada!
echo.
echo 🚀 Para iniciar los servicios:
echo.
echo 📍 PASO 1: Abrir una nueva ventana de PowerShell/CMD
echo   cd backend
echo   venv\Scripts\activate
echo   python main.py
echo.
echo 📍 PASO 2: Abrir otra ventana de PowerShell/CMD
echo   cd frontend
echo   npm run dev
echo.
echo 📊 URLs disponibles:
echo • Frontend: http://localhost:5173
echo • Backend API: http://localhost:8000
echo • Documentación: http://localhost:8000/docs
echo.
echo ¿Quieres abrir VS Code ahora? (s/n)
set /p opencode=
if /i "%opencode%"=="s" code .
goto end

:vscode_setup
echo.
echo 📱 Configurando VS Code Extensions...
echo.

:: Verificar VS Code
code --version >nul 2>&1
if errorlevel 1 (
    echo ❌ VS Code no está disponible desde terminal.
    echo Instala VS Code y añádelo al PATH, o instala manualmente las extensiones.
    echo 📋 Lista de extensiones en: VSCODE_EXTENSIONS.md
    pause
    goto end
)

echo 🔌 Instalando extensiones esenciales...

:: Instalar extensiones
code --install-extension ritwickdey.LiveServer
code --install-extension ms-python.python
code --install-extension ms-azuretools.vscode-docker
code --install-extension humao.rest-client
code --install-extension qwtel.sqlite-viewer
code --install-extension rangav.vscode-thunder-client
code --install-extension ms-python.debugpy

echo.
echo ✅ Extensiones instaladas y configuradas
echo.
echo 🚀 Usar VS Code:
echo 1. Abre el proyecto en VS Code
echo 2. Ve a Terminal → New Terminal
echo 3. Ejecuta los comandos de la opción 2 (Local setup)
echo 4. Usa F5 para debug del backend
echo 5. Click derecho en index.html → 'Open with Live Server'
echo.
code .
goto end

:codespaces_setup
echo.
echo 🌐 Configurando para GitHub Codespaces...
echo.
echo ✅ Configuración de Codespaces creada
echo.
echo 🚀 Pasos siguientes:
echo 1. Haz commit de los cambios a tu repositorio
echo 2. Ve a GitHub.com → tu repositorio
echo 3. Click en 'Code' → 'Codespaces' → 'Create codespace'
echo 4. ¡Espera a que se configure automáticamente!
echo.
echo 💡 Tienes 60 horas GRATIS por mes
echo.
pause
start https://github.com
goto end

:invalid
echo.
echo ❌ Opción inválida
timeout /t 2 >nul
goto start

:exit
echo.
echo 👋 ¡Hasta luego!
goto end

:end
echo.
echo Presiona cualquier tecla para salir...
pause >nul
