# Etapa 1: Build del frontend
FROM node:18-alpine as build

WORKDIR /app

# Copiar archivos de dependencias
COPY frontend/package*.json ./

# Instalar dependencias
RUN npm ci --only=production

# Copiar código fuente
COPY frontend/ .

# Build de producción
RUN npm run build

# Etapa 2: Servidor nginx
FROM nginx:alpine

# Copiar archivos build
COPY --from=build /app/dist /usr/share/nginx/html

# Copiar configuración de nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Exponer puerto
EXPOSE 80

# Comando por defecto
CMD ["nginx", "-g", "daemon off;"]
