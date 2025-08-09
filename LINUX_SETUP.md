# 🐧 Opciones Linux GRATUITAS para Desarrollo

## 1. **WSL2 (Windows Subsystem for Linux)** ⭐ RECOMENDADO
- **Costo**: GRATIS (ya tienes Windows)
- **Ventajas**: Linux nativo dentro de Windows
- **Instalación**:

```powershell
# Habilitar WSL2
wsl --install Ubuntu-22.04

# Después de reiniciar, configurar usuario
# Instalar dependencias en Ubuntu:
sudo apt update && sudo apt upgrade -y
sudo apt install python3.9 python3.9-venv python3-pip nodejs npm nginx sqlite3 -y

# Clonar proyecto
cd /home/tu-usuario
git clone https://github.com/tu-usuario/pymes-risk.git
cd pymes-risk

# Configurar backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configurar frontend
cd ../frontend
npm install
npm run dev
```

## 2. **VirtualBox + Ubuntu** 
- **Costo**: GRATIS
- **Specs**: Según tu PC (recomendado 4GB RAM mínimo)
- **Pasos**:
  1. Descargar VirtualBox: https://www.virtualbox.org/
  2. Descargar Ubuntu 22.04: https://ubuntu.com/download/desktop
  3. Crear máquina virtual con 4GB RAM, 20GB disco
  4. Instalar Ubuntu
  5. Seguir pasos de instalación de dependencias

## 3. **VMware Workstation Player** (Gratis para uso personal)
- **Costo**: GRATIS (uso personal)
- **Ventajas**: Mejor rendimiento que VirtualBox

## 4. **Multipass** (Ubuntu VM Manager)
- **Costo**: GRATIS
- **Ventajas**: VMs Ubuntu ligeras y rápidas

```bash
# Instalar Multipass
# Descargar desde: https://multipass.run/

# Crear VM Ubuntu
multipass launch --name pymes-dev --cpus 2 --mem 4G --disk 20G

# Entrar a la VM
multipass shell pymes-dev

# Instalar dependencias
sudo apt update
sudo apt install python3.9 python3.9-venv python3-pip nodejs npm nginx sqlite3 git -y

# Transferir archivos del proyecto
# Desde Windows PowerShell:
multipass transfer ./proyecto pymes-dev:/home/ubuntu/pymes-risk
```

## Script de Configuración Automática para Linux

```bash
#!/bin/bash
# setup-pymes-dev.sh - Script para configurar entorno de desarrollo

echo "🚀 Configurando entorno de desarrollo PyMEs Risk Assessment..."

# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias base
sudo apt install -y curl wget git python3.9 python3.9-venv python3-pip nodejs npm nginx sqlite3 postgresql postgresql-contrib redis-server

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Crear directorio del proyecto
mkdir -p ~/pymes-risk-dev
cd ~/pymes-risk-dev

# Configurar Git (si es necesario)
echo "Configurando Git..."
read -p "Tu nombre para Git: " git_name
read -p "Tu email para Git: " git_email
git config --global user.name "$git_name"
git config --global user.email "$git_email"

echo "✅ Entorno configurado. Clona tu proyecto con:"
echo "git clone https://github.com/tu-usuario/pymes-risk.git"
echo ""
echo "🐳 Para usar Docker:"
echo "cd pymes-risk && docker-compose -f docker-compose.dev.yml up"
```
