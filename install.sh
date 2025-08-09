#!/bin/bash

# =============================================================================
# Script de Instalación Automatizada
# Sistema de Evaluación Inteligente de Riesgo Financiero para PYMEs
# =============================================================================

set -e  # Salir si hay errores

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funciones de utilidad
print_header() {
    echo -e "\n${BLUE}=====================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}=====================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Verificar si el script se ejecuta como root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        print_error "Este script no debe ejecutarse como root. Úsalo con un usuario con permisos sudo."
        exit 1
    fi
}

# Detectar sistema operativo
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if [ -f /etc/ubuntu-release ] || [ -f /etc/debian_version ]; then
            OS="ubuntu"
            print_success "Sistema detectado: Ubuntu/Debian"
        elif [ -f /etc/redhat-release ] || [ -f /etc/centos-release ]; then
            OS="centos"
            print_success "Sistema detectado: CentOS/RHEL"
        else
            print_error "Distribución Linux no soportada"
            exit 1
        fi
    else
        print_error "Sistema operativo no soportado. Este script está diseñado para Linux."
        exit 1
    fi
}

# Instalar dependencias del sistema
install_system_dependencies() {
    print_header "INSTALANDO DEPENDENCIAS DEL SISTEMA"
    
    if [ "$OS" = "ubuntu" ]; then
        sudo apt update
        sudo apt install -y curl wget git nginx certbot python3-certbot-nginx \
                            python3.8 python3.8-venv python3.8-dev python3-pip \
                            sqlite3 ufw software-properties-common
    elif [ "$OS" = "centos" ]; then
        sudo yum update -y
        sudo yum install -y curl wget git nginx certbot python3-certbot-nginx \
                           python38 python38-pip sqlite firewalld
    fi
    
    print_success "Dependencias del sistema instaladas"
}

# Instalar Node.js
install_nodejs() {
    print_header "INSTALANDO NODE.JS"
    
    # Instalar Node.js 18.x
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    
    if [ "$OS" = "ubuntu" ]; then
        sudo apt-get install -y nodejs
    elif [ "$OS" = "centos" ]; then
        sudo yum install -y nodejs npm
    fi
    
    # Verificar instalación
    node_version=$(node --version)
    npm_version=$(npm --version)
    
    print_success "Node.js $node_version instalado"
    print_success "npm $npm_version instalado"
}

# Configurar proyecto
setup_project() {
    print_header "CONFIGURANDO PROYECTO"
    
    # Crear directorio del proyecto
    sudo mkdir -p /var/www/pymes-risk
    sudo chown $USER:$USER /var/www/pymes-risk
    
    # Si el proyecto ya existe, hacer backup
    if [ -d "/var/www/pymes-risk/backend" ]; then
        print_warning "Proyecto existente encontrado. Creando backup..."
        sudo mv /var/www/pymes-risk /var/www/pymes-risk.backup.$(date +%Y%m%d_%H%M%S)
        sudo mkdir -p /var/www/pymes-risk
        sudo chown $USER:$USER /var/www/pymes-risk
    fi
    
    cd /var/www/pymes-risk
    
    # Copiar archivos del proyecto (asumiendo que están en el directorio actual)
    if [ -d "$HOME/Reto-2---Evaluaci-n-Inteligente-de-Riesgo-Financiero-para-PYMEs" ]; then
        cp -r "$HOME/Reto-2---Evaluaci-n-Inteligente-de-Riesgo-Financiero-para-PYMEs"/* .
    else
        print_error "No se encontró el directorio del proyecto. Asegúrate de que esté en $HOME/"
        exit 1
    fi
    
    print_success "Proyecto copiado a /var/www/pymes-risk"
}

# Configurar backend
setup_backend() {
    print_header "CONFIGURANDO BACKEND"
    
    cd /var/www/pymes-risk/backend
    
    # Crear entorno virtual
    python3 -m venv venv
    source venv/bin/activate
    
    # Actualizar pip
    pip install --upgrade pip
    
    # Instalar dependencias
    pip install -r requirements.txt
    
    # Crear directorios necesarios
    mkdir -p database uploads logs
    
    # Configurar variables de entorno
    cat > .env << EOF
DATABASE_URL=sqlite:///./database/pymes_risk.db
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=production
SECRET_KEY=$(openssl rand -hex 32)
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
UPLOAD_MAX_SIZE=10485760
LOG_LEVEL=INFO
EOF
    
    # Cambiar permisos
    sudo chown -R www-data:www-data /var/www/pymes-risk
    sudo chmod -R 755 /var/www/pymes-risk
    
    print_success "Backend configurado"
}

# Configurar frontend
setup_frontend() {
    print_header "CONFIGURANDO FRONTEND"
    
    cd /var/www/pymes-risk/frontend
    
    # Instalar dependencias
    npm install
    
    # Configurar variables de entorno
    cat > .env << EOF
VITE_API_URL=http://localhost:8000/api/v1
VITE_APP_NAME=PyMEs Risk Assessment
VITE_ENVIRONMENT=production
EOF
    
    # Construir para producción
    npm run build
    
    print_success "Frontend configurado y construido"
}

# Configurar servicio systemd
setup_systemd_service() {
    print_header "CONFIGURANDO SERVICIO SYSTEMD"
    
    sudo tee /etc/systemd/system/pymes-backend.service > /dev/null << EOF
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
ExecReload=/bin/kill -HUP \$MAINPID
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF
    
    # Activar y iniciar servicio
    sudo systemctl daemon-reload
    sudo systemctl enable pymes-backend
    sudo systemctl start pymes-backend
    
    # Verificar estado
    sleep 5
    if sudo systemctl is-active --quiet pymes-backend; then
        print_success "Servicio backend iniciado correctamente"
    else
        print_error "Error al iniciar el servicio backend"
        sudo systemctl status pymes-backend
        exit 1
    fi
}

# Configurar Nginx
setup_nginx() {
    print_header "CONFIGURANDO NGINX"
    
    # Crear configuración de Nginx
    sudo tee /etc/nginx/sites-available/pymes-risk > /dev/null << 'EOF'
server {
    listen 80;
    server_name localhost;
    
    # Frontend
    location / {
        root /var/www/pymes-risk/frontend/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
        
        # Cache para archivos estáticos
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
    
    # Backend API
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        client_max_body_size 10M;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
}
EOF
    
    # Activar sitio
    sudo ln -sf /etc/nginx/sites-available/pymes-risk /etc/nginx/sites-enabled/
    
    # Remover sitio por defecto
    sudo rm -f /etc/nginx/sites-enabled/default
    
    # Verificar configuración
    if sudo nginx -t; then
        print_success "Configuración de Nginx válida"
        sudo systemctl reload nginx
        print_success "Nginx recargado"
    else
        print_error "Error en la configuración de Nginx"
        exit 1
    fi
}

# Configurar firewall
setup_firewall() {
    print_header "CONFIGURANDO FIREWALL"
    
    if [ "$OS" = "ubuntu" ]; then
        sudo ufw --force enable
        sudo ufw allow ssh
        sudo ufw allow 'Nginx Full'
        sudo ufw status
    elif [ "$OS" = "centos" ]; then
        sudo systemctl start firewalld
        sudo systemctl enable firewalld
        sudo firewall-cmd --permanent --add-service=http
        sudo firewall-cmd --permanent --add-service=https
        sudo firewall-cmd --permanent --add-service=ssh
        sudo firewall-cmd --reload
    fi
    
    print_success "Firewall configurado"
}

# Configurar backups
setup_backups() {
    print_header "CONFIGURANDO BACKUPS AUTOMÁTICOS"
    
    # Crear directorio de backups
    sudo mkdir -p /var/backups/pymes-risk
    
    # Crear script de backup
    sudo tee /usr/local/bin/backup-pymes.sh > /dev/null << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/pymes-risk"
PROJECT_DIR="/var/www/pymes-risk"

mkdir -p $BACKUP_DIR

# Backup base de datos
if [ -f "$PROJECT_DIR/backend/database/pymes_risk.db" ]; then
    sqlite3 "$PROJECT_DIR/backend/database/pymes_risk.db" ".backup $BACKUP_DIR/database_$DATE.db"
fi

# Backup archivos subidos
if [ -d "$PROJECT_DIR/backend/uploads" ]; then
    tar -czf "$BACKUP_DIR/uploads_$DATE.tar.gz" -C "$PROJECT_DIR/backend" uploads/
fi

# Mantener solo últimos 7 días
find $BACKUP_DIR -name "*.db" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completado: $DATE"
EOF
    
    # Hacer ejecutable
    sudo chmod +x /usr/local/bin/backup-pymes.sh
    
    # Programar en crontab
    echo "0 2 * * * /usr/local/bin/backup-pymes.sh >> /var/log/backup-pymes.log 2>&1" | sudo crontab -
    
    print_success "Backups automáticos configurados (diario a las 2 AM)"
}

# Verificar instalación
verify_installation() {
    print_header "VERIFICANDO INSTALACIÓN"
    
    # Verificar servicios
    echo "Verificando servicios..."
    
    if sudo systemctl is-active --quiet pymes-backend; then
        print_success "Servicio backend: ACTIVO"
    else
        print_error "Servicio backend: INACTIVO"
    fi
    
    if sudo systemctl is-active --quiet nginx; then
        print_success "Servicio nginx: ACTIVO"
    else
        print_error "Servicio nginx: INACTIVO"
    fi
    
    # Verificar puertos
    echo -e "\nVerificando puertos..."
    
    if netstat -tulpn | grep -q ":8000"; then
        print_success "Puerto 8000 (backend): ABIERTO"
    else
        print_error "Puerto 8000 (backend): CERRADO"
    fi
    
    if netstat -tulpn | grep -q ":80"; then
        print_success "Puerto 80 (nginx): ABIERTO"
    else
        print_error "Puerto 80 (nginx): CERRADO"
    fi
    
    # Test de conectividad
    echo -e "\nRealizando tests de conectividad..."
    
    if curl -s http://localhost:8000/api/v1/health > /dev/null; then
        print_success "API backend: RESPONDE"
    else
        print_warning "API backend: NO RESPONDE (puede tardar unos segundos en iniciar)"
    fi
    
    if curl -s http://localhost/ > /dev/null; then
        print_success "Frontend: ACCESIBLE"
    else
        print_error "Frontend: NO ACCESIBLE"
    fi
}

# Mostrar información final
show_final_info() {
    print_header "INSTALACIÓN COMPLETADA"
    
    echo -e "${GREEN}🎉 ¡Sistema instalado correctamente!${NC}\n"
    
    echo -e "${BLUE}Información del sistema:${NC}"
    echo -e "• Frontend: ${GREEN}http://localhost/${NC}"
    echo -e "• Backend API: ${GREEN}http://localhost:8000/api/v1/${NC}"
    echo -e "• Documentación API: ${GREEN}http://localhost:8000/docs${NC}"
    echo -e "• Archivos del proyecto: ${GREEN}/var/www/pymes-risk/${NC}"
    echo -e "• Logs del backend: ${GREEN}sudo journalctl -f -u pymes-backend${NC}"
    echo -e "• Logs de nginx: ${GREEN}sudo tail -f /var/log/nginx/access.log${NC}"
    
    echo -e "\n${BLUE}Comandos útiles:${NC}"
    echo -e "• Reiniciar backend: ${YELLOW}sudo systemctl restart pymes-backend${NC}"
    echo -e "• Reiniciar nginx: ${YELLOW}sudo systemctl restart nginx${NC}"
    echo -e "• Ver estado: ${YELLOW}sudo systemctl status pymes-backend${NC}"
    echo -e "• Backup manual: ${YELLOW}sudo /usr/local/bin/backup-pymes.sh${NC}"
    
    echo -e "\n${BLUE}Próximos pasos:${NC}"
    echo -e "1. ${GREEN}Configurar dominio${NC} (opcional): Editar /etc/nginx/sites-available/pymes-risk"
    echo -e "2. ${GREEN}Configurar SSL${NC} (recomendado): sudo certbot --nginx -d tu-dominio.com"
    echo -e "3. ${GREEN}Monitorear logs${NC}: sudo journalctl -f -u pymes-backend"
    echo -e "4. ${GREEN}Acceder al sistema${NC}: http://localhost/"
    
    echo -e "\n${GREEN}¡El sistema está listo para evaluar el riesgo financiero de PYMEs! 🚀${NC}"
}

# Función principal
main() {
    print_header "INSTALACIÓN AUTOMÁTICA - SISTEMA PYMES RISK ASSESSMENT"
    
    echo -e "${BLUE}Este script instalará automáticamente el sistema completo.${NC}"
    echo -e "${YELLOW}Presiona ENTER para continuar o Ctrl+C para cancelar...${NC}"
    read
    
    check_root
    detect_os
    install_system_dependencies
    install_nodejs
    setup_project
    setup_backend
    setup_frontend
    setup_systemd_service
    setup_nginx
    setup_firewall
    setup_backups
    verify_installation
    show_final_info
}

# Ejecutar si es llamado directamente
if [ "${BASH_SOURCE[0]}" == "${0}" ]; then
    main "$@"
fi
