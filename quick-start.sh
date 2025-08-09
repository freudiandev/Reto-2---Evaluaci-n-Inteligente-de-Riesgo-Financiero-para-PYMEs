#!/bin/bash

# =============================================================================
# 🚀 INICIO RÁPIDO - PyMEs Risk Assessment
# Script para levantar el proyecto localmente SIN COSTO
# =============================================================================

set -e

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

clear
echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║              🏦 PyMEs Risk Assessment                      ║"
echo "║           🚀 INICIO RÁPIDO - DESARROLLO LOCAL              ║"
echo "║                        GRATUITO                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}\n"

# Función para mostrar opciones
show_menu() {
    echo -e "${YELLOW}Selecciona tu opción de desarrollo GRATUITA:${NC}\n"
    echo "1. 🐳 Docker Compose (Recomendado - Simula servidor completo)"
    echo "2. 🐍 Python Local + Node.js (Simple y rápido)"
    echo "3. 🌐 GitHub Codespaces (En la nube - 60h gratis/mes)"
    echo "4. 🐧 WSL2 Ubuntu (Linux en Windows)"
    echo "5. 📱 Solo VS Code Extensions (Más básico)"
    echo "6. ❌ Salir"
    echo
    read -p "Tu elección (1-6): " choice
}

# Opción 1: Docker Compose
docker_setup() {
    echo -e "${BLUE}🐳 Configurando con Docker Compose...${NC}"
    
    # Verificar Docker
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker no está instalado.${NC}"
        echo "Instala Docker Desktop desde: https://www.docker.com/products/docker-desktop"
        echo "Es GRATIS para uso personal."
        exit 1
    fi
    
    # Verificar Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        echo -e "${RED}❌ Docker Compose no está instalado.${NC}"
        echo "Viene incluido con Docker Desktop."
        exit 1
    fi
    
    echo -e "${GREEN}✅ Docker detectado${NC}"
    
    # Construir y levantar servicios
    echo "🔨 Construyendo contenedores..."
    docker-compose -f docker-compose.dev.yml build
    
    echo "🚀 Levantando servicios..."
    docker-compose -f docker-compose.dev.yml up -d
    
    echo -e "\n${GREEN}🎉 ¡Servicios iniciados exitosamente!${NC}"
    echo -e "\n📊 URLs disponibles:"
    echo -e "• Frontend: ${GREEN}http://localhost${NC} (Nginx proxy)"
    echo -e "• Backend API: ${GREEN}http://localhost:8000${NC}"
    echo -e "• Documentación: ${GREEN}http://localhost:8000/docs${NC}"
    echo -e "• Base de datos: ${GREEN}http://localhost:8080${NC} (Adminer)"
    echo -e "• Vite Dev: ${GREEN}http://localhost:5173${NC} (directo)"
    
    echo -e "\n🔧 Comandos útiles:"
    echo "• Ver logs: docker-compose -f docker-compose.dev.yml logs -f"
    echo "• Detener: docker-compose -f docker-compose.dev.yml down"
    echo "• Reiniciar: docker-compose -f docker-compose.dev.yml restart"
}

# Opción 2: Local con Python y Node.js
local_setup() {
    echo -e "${BLUE}🐍 Configurando desarrollo local...${NC}"
    
    # Verificar Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python3 no está instalado.${NC}"
        echo "Instala Python desde: https://www.python.org/downloads/"
        exit 1
    fi
    
    # Verificar Node.js
    if ! command -v node &> /dev/null; then
        echo -e "${RED}❌ Node.js no está instalado.${NC}"
        echo "Instala Node.js desde: https://nodejs.org/"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Python y Node.js detectados${NC}"
    
    # Configurar backend
    echo "🔨 Configurando backend..."
    cd backend
    
    # Crear entorno virtual si no existe
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi
    
    # Activar entorno virtual
    source venv/bin/activate || . venv/Scripts/activate
    
    # Instalar dependencias
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # Crear directorios
    mkdir -p database uploads logs
    
    # Crear archivo .env si no existe
    if [ ! -f ".env" ]; then
        cat > .env << EOF
DATABASE_URL=sqlite:///./database/pymes_risk.db
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
EOF
    fi
    
    cd ..
    
    # Configurar frontend
    echo "🔨 Configurando frontend..."
    cd frontend
    npm install
    
    # Crear archivo .env si no existe
    if [ ! -f ".env" ]; then
        cat > .env << EOF
VITE_API_URL=http://localhost:8000/api/v1
VITE_APP_NAME=PyMEs Risk Assessment
VITE_ENVIRONMENT=development
EOF
    fi
    
    cd ..
    
    echo -e "\n${GREEN}🎉 ¡Configuración completada!${NC}"
    echo -e "\n🚀 Para iniciar los servicios:"
    echo "📍 Terminal 1 (Backend):"
    echo "  cd backend && source venv/bin/activate && python main.py"
    echo
    echo "📍 Terminal 2 (Frontend):"
    echo "  cd frontend && npm run dev"
    echo
    echo -e "📊 URLs disponibles:"
    echo -e "• Frontend: ${GREEN}http://localhost:5173${NC}"
    echo -e "• Backend API: ${GREEN}http://localhost:8000${NC}"
    echo -e "• Documentación: ${GREEN}http://localhost:8000/docs${NC}"
}

# Opción 3: GitHub Codespaces
codespaces_setup() {
    echo -e "${BLUE}🌐 Configurando para GitHub Codespaces...${NC}"
    
    # Crear directorio .devcontainer si no existe
    mkdir -p .devcontainer
    
    # Crear configuración de devcontainer
    cat > .devcontainer/devcontainer.json << 'EOF'
{
    "name": "PyMEs Risk Assessment",
    "image": "mcr.microsoft.com/vscode/devcontainers/python:3.9",
    "features": {
        "ghcr.io/devcontainers/features/node:1": {
            "version": "18"
        },
        "ghcr.io/devcontainers/features/docker-in-docker:2": {}
    },
    "postCreateCommand": "pip install -r backend/requirements.txt && cd frontend && npm install",
    "forwardPorts": [8000, 5173, 3000],
    "portsAttributes": {
        "8000": {
            "label": "Backend API",
            "onAutoForward": "notify"
        },
        "5173": {
            "label": "Frontend Dev",
            "onAutoForward": "openBrowser"
        }
    },
    "customizations": {
        "vscode": {
            "extensions": [
                "ms-python.python",
                "ms-python.debugpy",
                "ms-azuretools.vscode-docker",
                "humao.rest-client",
                "rangav.vscode-thunder-client",
                "qwtel.sqlite-viewer"
            ]
        }
    }
}
EOF
    
    echo -e "${GREEN}✅ Configuración de Codespaces creada${NC}"
    echo -e "\n🚀 Pasos siguientes:"
    echo "1. Haz commit de los cambios a tu repositorio"
    echo "2. Ve a GitHub.com → tu repositorio"
    echo "3. Click en 'Code' → 'Codespaces' → 'Create codespace'"
    echo "4. ¡Espera a que se configure automáticamente!"
    echo
    echo -e "${YELLOW}💡 Tienes 60 horas GRATIS por mes${NC}"
}

# Opción 4: WSL2
wsl_setup() {
    echo -e "${BLUE}🐧 Configurando para WSL2...${NC}"
    
    # Verificar si estamos en WSL
    if grep -q Microsoft /proc/version 2>/dev/null; then
        echo -e "${GREEN}✅ Ya estás en WSL${NC}"
        local_setup
    else
        echo -e "${YELLOW}ℹ️  Configuración para WSL2 desde Windows${NC}"
        echo
        echo "🔧 Pasos para configurar WSL2:"
        echo "1. Abre PowerShell como Administrador"
        echo "2. Ejecuta: wsl --install Ubuntu-22.04"
        echo "3. Reinicia tu PC"
        echo "4. Configura usuario y contraseña en Ubuntu"
        echo "5. Ejecuta este script de nuevo desde Ubuntu"
        echo
        echo "📖 Guía completa: https://docs.microsoft.com/en-us/windows/wsl/install"
    fi
}

# Opción 5: VS Code Extensions
vscode_setup() {
    echo -e "${BLUE}📱 Configurando VS Code Extensions...${NC}"
    
    # Verificar VS Code
    if ! command -v code &> /dev/null; then
        echo -e "${RED}❌ VS Code no está disponible desde terminal.${NC}"
        echo "Instala VS Code y añádelo al PATH, o instala manualmente las extensiones."
        echo "📋 Lista de extensiones en: VSCODE_EXTENSIONS.md"
        exit 1
    fi
    
    echo "🔌 Instalando extensiones esenciales..."
    
    # Lista de extensiones
    extensions=(
        "ritwickdey.LiveServer"
        "ms-python.python"
        "ms-azuretools.vscode-docker"
        "humao.rest-client"
        "qwtel.sqlite-viewer"
        "rangav.vscode-thunder-client"
        "ms-python.debugpy"
    )
    
    for ext in "${extensions[@]}"; do
        echo "Instalando $ext..."
        code --install-extension "$ext"
    done
    
    # Crear configuración de workspace
    mkdir -p .vscode
    
    cat > .vscode/settings.json << 'EOF'
{
    "python.defaultInterpreterPath": "./backend/venv/Scripts/python.exe",
    "python.terminal.activateEnvironment": true,
    "liveServer.settings.port": 5173,
    "liveServer.settings.root": "/frontend/dist",
    "rest-client.environmentVariables": {
        "local": {
            "baseUrl": "http://localhost:8000",
            "apiUrl": "http://localhost:8000/api/v1"
        }
    }
}
EOF
    
    cat > .vscode/launch.json << 'EOF'
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/backend/main.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}/backend"
        }
    ]
}
EOF
    
    echo -e "\n${GREEN}✅ Extensiones instaladas y configuradas${NC}"
    echo -e "\n🚀 Usar VS Code:"
    echo "1. Abre el proyecto en VS Code"
    echo "2. Ve a Terminal → New Terminal"
    echo "3. Ejecuta los comandos de la opción 2 (Local setup)"
    echo "4. Usa F5 para debug del backend"
    echo "5. Click derecho en index.html → 'Open with Live Server'"
}

# Función principal
main() {
    show_menu
    
    case $choice in
        1)
            docker_setup
            ;;
        2)
            local_setup
            ;;
        3)
            codespaces_setup
            ;;
        4)
            wsl_setup
            ;;
        5)
            vscode_setup
            ;;
        6)
            echo -e "${YELLOW}👋 ¡Hasta luego!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Opción inválida${NC}"
            main
            ;;
    esac
}

# Ejecutar
main
