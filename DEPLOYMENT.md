# 🚀 Guía de Despliegue en Servidor

## 📋 Opciones de Despliegue

### 1. **Servidor Linux (Ubuntu/CentOS) - RECOMENDADO**
### 2. **Docker & Docker Compose**
### 3. **Servicios en la Nube (AWS, Azure, GCP)**
### 4. **VPS (DigitalOcean, Linode, Vultr)**

---

## 🐧 OPCIÓN 1: Servidor Linux (Ubuntu 20.04/22.04)

### Prerrequisitos del Servidor
```bash
# Especificaciones mínimas recomendadas:
- CPU: 2 cores
- RAM: 4GB
- Almacenamiento: 20GB SSD
- Sistema: Ubuntu 20.04+ / CentOS 8+
- Acceso root o sudo
```

### 1. Actualización del Sistema
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install curl wget git nginx certbot python3-certbot-nginx -y
```

### 2. Instalación de Python 3.8+
```bash
# Verificar versión
python3 --version

# Si necesitas instalar Python 3.8+
sudo apt install python3.8 python3.8-venv python3.8-dev python3-pip -y

# Crear enlace simbólico (si es necesario)
sudo ln -sf /usr/bin/python3.8 /usr/bin/python3
```

### 3. Instalación de Node.js 16+
```bash
# Instalar Node.js usando NodeSource
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verificar instalación
node --version
npm --version
```

### 4. Configuración del Proyecto

#### A. Clonar/Subir el Proyecto
```bash
# Crear directorio para aplicaciones
sudo mkdir -p /var/www/pymes-risk
sudo chown $USER:$USER /var/www/pymes-risk
cd /var/www/pymes-risk

# Si usas Git (recomendado)
git clone https://tu-repositorio.com/pymes-risk-assessment.git .

# O subir archivos vía SCP/SFTP
# scp -r ./proyecto user@servidor:/var/www/pymes-risk/
```

#### B. Configuración del Backend
```bash
cd /var/www/pymes-risk/backend

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Crear directorios necesarios
mkdir -p database uploads logs

# Configurar variables de entorno
nano .env
```

**Archivo .env del Backend:**
```bash
DATABASE_URL=sqlite:///./database/pymes_risk.db
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=production
SECRET_KEY=tu-clave-secreta-muy-segura-aqui
CORS_ORIGINS=https://tu-dominio.com,https://www.tu-dominio.com
UPLOAD_MAX_SIZE=10485760
LOG_LEVEL=INFO
```

#### C. Configuración del Frontend
```bash
cd /var/www/pymes-risk/frontend

# Instalar dependencias
npm install

# Configurar variables de entorno
nano .env
```

**Archivo .env del Frontend:**
```bash
VITE_API_URL=https://api.tu-dominio.com/api/v1
VITE_APP_NAME=PyMEs Risk Assessment
VITE_ENVIRONMENT=production
```

```bash
# Construir para producción
npm run build

# Los archivos compilados estarán en ./dist/
```

### 5. Configuración de Servicios (systemd)

#### A. Servicio del Backend
```bash
sudo nano /etc/systemd/system/pymes-backend.service
```

```ini
[Unit]
Description=PyMEs Risk Assessment Backend
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/pymes-risk/backend
Environment=PATH=/var/www/pymes-risk/backend/venv/bin
ExecStart=/var/www/pymes-risk/backend/venv/bin/python main.py
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

```bash
# Activar y iniciar el servicio
sudo systemctl daemon-reload
sudo systemctl enable pymes-backend
sudo systemctl start pymes-backend
sudo systemctl status pymes-backend
```

### 6. Configuración de Nginx

#### A. Configuración del sitio
```bash
sudo nano /etc/nginx/sites-available/pymes-risk
```

```nginx
# Backend API
server {
    listen 80;
    server_name api.tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        # Configuración para archivos grandes
        client_max_body_size 10M;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}

# Frontend
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;
    root /var/www/pymes-risk/frontend/dist;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    # Static files caching
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # SPA fallback
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
}
```

```bash
# Activar sitio
sudo ln -s /etc/nginx/sites-available/pymes-risk /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 7. Configuración SSL con Let's Encrypt
```bash
# Obtener certificados SSL
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com -d api.tu-dominio.com

# Configurar renovación automática
sudo crontab -e
# Añadir: 0 12 * * * /usr/bin/certbot renew --quiet
```

### 8. Configuración de Firewall
```bash
# UFW (Ubuntu)
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw status

# Firewalld (CentOS)
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --reload
```

---

## 🐳 OPCIÓN 2: Docker & Docker Compose

### 1. Crear Dockerfile para Backend
```dockerfile
# backend/Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Crear directorios necesarios
RUN mkdir -p database uploads logs

# Exponer puerto
EXPOSE 8000

# Comando de inicio
CMD ["python", "main.py"]
```

### 2. Crear Dockerfile para Frontend
```dockerfile
# frontend/Dockerfile
FROM node:18-alpine as builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

# Servidor de producción
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 3. Configuración de nginx para Frontend
```nginx
# frontend/nginx.conf
events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    server {
        listen 80;
        server_name localhost;
        root /usr/share/nginx/html;
        index index.html;

        location / {
            try_files $uri $uri/ /index.html;
        }

        location /api {
            proxy_pass http://backend:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
}
```

### 4. Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./backend
    container_name: pymes-backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./database/pymes_risk.db
      - API_HOST=0.0.0.0
      - API_PORT=8000
      - ENVIRONMENT=production
    volumes:
      - ./backend/database:/app/database
      - ./backend/uploads:/app/uploads
    restart: unless-stopped

  frontend:
    build: ./frontend
    container_name: pymes-frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped

  nginx-proxy:
    image: nginx:alpine
    container_name: nginx-proxy
    ports:
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend
    restart: unless-stopped
```

### 5. Comandos de Despliegue con Docker
```bash
# Construir y ejecutar
docker-compose up -d --build

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down

# Actualizar aplicación
git pull
docker-compose down
docker-compose up -d --build
```

---

## ☁️ OPCIÓN 3: Servicios en la Nube

### AWS (Amazon Web Services)

#### Backend en EC2 + RDS
```bash
# 1. Lanzar instancia EC2 (t3.small o superior)
# 2. Configurar Security Groups:
#    - HTTP: 80
#    - HTTPS: 443
#    - SSH: 22
#    - Custom: 8000 (temporal)

# 3. Instalar dependencias (seguir pasos de Linux)
# 4. Configurar RDS PostgreSQL (opcional)
# 5. Usar S3 para archivos subidos
```

#### Frontend en S3 + CloudFront
```bash
# 1. Crear bucket S3 para hosting estático
aws s3 mb s3://pymes-risk-frontend

# 2. Configurar como sitio web estático
aws s3 website s3://pymes-risk-frontend --index-document index.html

# 3. Subir archivos compilados
cd frontend
npm run build
aws s3 sync dist/ s3://pymes-risk-frontend

# 4. Configurar CloudFront para CDN
# 5. Configurar Route 53 para dominio
```

### Azure

#### Backend en App Service
```bash
# 1. Crear App Service Plan
az appservice plan create --name pymes-backend-plan --resource-group pymes-rg --sku B1

# 2. Crear Web App
az webapp create --resource-group pymes-rg --plan pymes-backend-plan --name pymes-risk-api

# 3. Configurar despliegue desde Git
az webapp deployment source config --name pymes-risk-api --resource-group pymes-rg --repo-url https://github.com/tu-repo.git --branch main
```

#### Frontend en Static Web Apps
```bash
# 1. Crear Static Web App
az staticwebapp create --name pymes-risk-frontend --resource-group pymes-rg --source https://github.com/tu-repo.git --branch main --app-location "/frontend" --build-location "dist"
```

### Google Cloud Platform

#### Backend en Cloud Run
```bash
# 1. Construir imagen Docker
docker build -t gcr.io/tu-proyecto/pymes-backend ./backend

# 2. Subir a Container Registry
docker push gcr.io/tu-proyecto/pymes-backend

# 3. Desplegar en Cloud Run
gcloud run deploy pymes-backend --image gcr.io/tu-proyecto/pymes-backend --platform managed --region us-central1 --allow-unauthenticated
```

---

## 🔧 Configuraciones Adicionales

### Base de Datos PostgreSQL (Recomendado para Producción)

#### 1. Instalación
```bash
# Ubuntu
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Crear base de datos
sudo -u postgres psql
CREATE DATABASE pymes_risk;
CREATE USER pymes_user WITH ENCRYPTED PASSWORD 'password-muy-segura';
GRANT ALL PRIVILEGES ON DATABASE pymes_risk TO pymes_user;
\q
```

#### 2. Configuración Backend
```python
# backend/.env
DATABASE_URL=postgresql://pymes_user:password-muy-segura@localhost/pymes_risk
```

#### 3. Migración desde SQLite
```bash
cd backend
python -c "
from app.models.database import Base, engine
Base.metadata.create_all(bind=engine)
print('Tablas creadas exitosamente')
"
```

### Redis para Cache (Opcional)
```bash
# Instalación
sudo apt install redis-server

# Configuración backend
pip install redis
```

### Monitoreo y Logs

#### 1. Configurar Logs Centralizados
```bash
# Instalar Logrotate
sudo nano /etc/logrotate.d/pymes-risk

/var/www/pymes-risk/backend/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 0644 www-data www-data
    postrotate
        systemctl reload pymes-backend
    endscript
}
```

#### 2. Monitoreo con htop/top
```bash
sudo apt install htop
htop
```

### Backup Automático
```bash
# Script de backup
sudo nano /usr/local/bin/backup-pymes.sh

#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/pymes-risk"
PROJECT_DIR="/var/www/pymes-risk"

mkdir -p $BACKUP_DIR

# Backup base de datos
sqlite3 $PROJECT_DIR/backend/database/pymes_risk.db ".backup $BACKUP_DIR/database_$DATE.db"

# Backup archivos subidos
tar -czf $BACKUP_DIR/uploads_$DATE.tar.gz -C $PROJECT_DIR/backend uploads/

# Mantener solo últimos 7 días
find $BACKUP_DIR -name "*.db" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

# Hacer ejecutable
sudo chmod +x /usr/local/bin/backup-pymes.sh

# Programar en crontab
sudo crontab -e
# Añadir: 0 2 * * * /usr/local/bin/backup-pymes.sh
```

---

## 🎯 Verificación Post-Despliegue

### 1. Verificar Backend
```bash
# Estado del servicio
sudo systemctl status pymes-backend

# Logs en tiempo real
sudo journalctl -f -u pymes-backend

# Test de API
curl https://api.tu-dominio.com/api/v1/health
```

### 2. Verificar Frontend
```bash
# Estado de Nginx
sudo systemctl status nginx

# Logs de acceso
sudo tail -f /var/log/nginx/access.log

# Test en navegador
https://tu-dominio.com
```

### 3. Verificar SSL
```bash
# Test SSL
openssl s_client -connect tu-dominio.com:443 -servername tu-dominio.com

# Online: https://www.ssllabs.com/ssltest/
```

---

## ⚡ Optimizaciones de Rendimiento

### 1. Backend
```python
# Usar Gunicorn en lugar de Uvicorn directo
pip install gunicorn

# Crear archivo gunicorn.conf.py
bind = "0.0.0.0:8000"
workers = 2
worker_class = "uvicorn.workers.UvicornWorker"
max_requests = 1000
max_requests_jitter = 100
timeout = 30
```

### 2. Frontend
```javascript
// Lazy loading de rutas
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Companies = lazy(() => import('./pages/Companies'));

// Code splitting automático con Vite
// Configurar en vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          router: ['react-router-dom']
        }
      }
    }
  }
})
```

### 3. Nginx
```nginx
# Configuración de cache
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}

# Compresión
gzip on;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

# Rate limiting
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
location /api/ {
    limit_req zone=api burst=20 nodelay;
}
```

---

## 🆘 Solución de Problemas

### Problemas Comunes

#### 1. Error 502 Bad Gateway
```bash
# Verificar que el backend esté corriendo
sudo systemctl status pymes-backend

# Verificar logs
sudo journalctl -f -u pymes-backend

# Reiniciar servicio
sudo systemctl restart pymes-backend
```

#### 2. Archivos no se suben
```bash
# Verificar permisos
sudo chown -R www-data:www-data /var/www/pymes-risk/backend/uploads
sudo chmod -R 755 /var/www/pymes-risk/backend/uploads

# Verificar configuración Nginx
client_max_body_size 10M;
```

#### 3. Base de datos bloqueada
```bash
# SQLite
sudo fuser /var/www/pymes-risk/backend/database/pymes_risk.db
# Matar procesos si es necesario

# PostgreSQL
sudo -u postgres psql -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'pymes_risk';"
```

### Comandos Útiles de Diagnóstico
```bash
# Uso de recursos
htop
df -h
free -m

# Conexiones de red
netstat -tulpn | grep :8000
netstat -tulpn | grep :80

# Logs del sistema
sudo journalctl -xe
sudo tail -f /var/log/nginx/error.log
```

---

## 📞 Soporte Post-Despliegue

### Documentación de Operaciones
1. **Monitoreo diario**: Verificar logs y métricas
2. **Backups**: Automatizados diariamente a las 2 AM
3. **Actualizaciones**: Proceso git pull + restart servicios
4. **Escalabilidad**: Agregar más workers o instancias según demanda

### Contactos de Emergencia
- **Administrador del Sistema**: [email/teléfono]
- **Desarrollador**: [email/teléfono]
- **Proveedor de Hosting**: [soporte técnico]

---

## 🎉 ¡Despliegue Completado!

Tu sistema de **Evaluación Inteligente de Riesgo Financiero para PYMEs** está ahora funcionando en producción con:

✅ **Backend API** funcionando en `https://api.tu-dominio.com`  
✅ **Frontend Dashboard** accesible en `https://tu-dominio.com`  
✅ **SSL/HTTPS** configurado y seguro  
✅ **Backups automáticos** programados  
✅ **Monitoreo** y logs configurados  
✅ **Rendimiento optimizado** para producción  

**¡El sistema está listo para evaluar el riesgo financiero de PYMEs con inteligencia artificial! 🚀**
