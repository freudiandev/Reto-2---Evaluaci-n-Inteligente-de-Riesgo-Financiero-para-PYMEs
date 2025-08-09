# 🚀 Extensiones VS Code para Desarrollo Local (GRATIS)

## Extensiones Esenciales para Simular Servidor

### 1. **Live Server** 
- **ID**: ritwickdey.LiveServer
- **Función**: Servidor web local con hot reload
- **Uso**: Click derecho → "Open with Live Server"

### 2. **Python**
- **ID**: ms-python.python
- **Función**: Soporte completo para Python
- **Incluye**: Debugger, linting, IntelliSense

### 3. **Docker**
- **ID**: ms-azuretools.vscode-docker
- **Función**: Gestión de contenedores Docker
- **Uso**: Click derecho en docker-compose.yml → "Compose Up"

### 4. **REST Client**
- **ID**: humao.rest-client
- **Función**: Probar APIs desde VS Code
- **Uso**: Crear archivos .http para testing

### 5. **SQLite Viewer**
- **ID**: qwtel.sqlite-viewer
- **Función**: Ver base de datos SQLite
- **Uso**: Click en archivo .db para abrirlo

### 6. **Thunder Client**
- **ID**: rangav.vscode-thunder-client
- **Función**: Cliente API como Postman
- **Uso**: Testing de endpoints

### 7. **Python Debugger**
- **ID**: ms-python.debugpy
- **Función**: Debug avanzado de Python
- **Uso**: Breakpoints y debugging

### 8. **ES6 String HTML**
- **ID**: Tobermory.es6-string-html
- **Función**: Syntax highlighting para HTML en JS/TS

### 9. **Auto Rename Tag**
- **ID**: formulahendry.auto-rename-tag
- **Función**: Renombra tags HTML automáticamente

### 10. **Bracket Pair Colorizer**
- **ID**: CoenraadS.bracket-pair-colorizer-2
- **Función**: Colorea brackets para mejor legibilidad

## Comandos para Instalar Todas las Extensiones

```bash
# Ejecutar en terminal de VS Code
code --install-extension ritwickdey.LiveServer
code --install-extension ms-python.python
code --install-extension ms-azuretools.vscode-docker
code --install-extension humao.rest-client
code --install-extension qwtel.sqlite-viewer
code --install-extension rangav.vscode-thunder-client
code --install-extension ms-python.debugpy
code --install-extension Tobermory.es6-string-html
code --install-extension formulahendry.auto-rename-tag
code --install-extension CoenraadS.bracket-pair-colorizer-2
```

## Configuración de Workspace

Crear archivo `.vscode/settings.json`:

```json
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
    },
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "emmet.includeLanguages": {
        "javascript": "javascriptreact",
        "typescript": "typescriptreact"
    }
}
```

## Configuración de Launch (Debug)

Crear archivo `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/backend/main.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}/backend",
            "env": {
                "PYTHONPATH": "${workspaceFolder}/backend"
            }
        },
        {
            "name": "Node: Vite Dev Server",
            "type": "node",
            "request": "launch",
            "program": "${workspaceFolder}/frontend/node_modules/.bin/vite",
            "args": ["--host", "0.0.0.0"],
            "cwd": "${workspaceFolder}/frontend",
            "runtimeExecutable": "npm",
            "runtimeArgs": ["run", "dev"]
        }
    ]
}
```
