# ☁️ Servicios de Cloud GRATUITOS para Desarrollo

## 1. **GitHub Codespaces** (RECOMENDADO)
- **Costo**: GRATIS (60 horas/mes)
- **Specs**: 2 cores, 4GB RAM, 32GB storage
- **Ventajas**: 
  - Entorno Linux completo
  - Pre-configurado con Python y Node.js
  - Acceso desde cualquier lugar
  - Integración perfecta con GitHub

### Configuración para Codespaces:
```json
// .devcontainer/devcontainer.json
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
                "rangav.vscode-thunder-client"
            ]
        }
    }
}
```

## 2. **Replit** 
- **Costo**: GRATIS
- **Specs**: Unlimited public repos
- **Ventajas**: IDE en navegador, colaboración en tiempo real

## 3. **GitPod**
- **Costo**: GRATIS (50 horas/mes)
- **Specs**: 4 cores, 8GB RAM
- **Ventajas**: Workspace pre-configurado

## 4. **Railway** (Para deploy gratuito)
- **Costo**: GRATIS ($5 crédito mensual)
- **Uso**: Deploy del backend Python

## 5. **Vercel** (Para frontend)
- **Costo**: GRATIS
- **Uso**: Deploy del frontend React

## 6. **PlanetScale** (Base de datos)
- **Costo**: GRATIS (1 base de datos)
- **Tipo**: MySQL serverless

## 7. **Supabase** (Backend alternativo)
- **Costo**: GRATIS
- **Incluye**: PostgreSQL + Auth + Storage
