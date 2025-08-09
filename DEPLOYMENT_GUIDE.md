# 🚀 Guía de Deployment Gratuito - PyMEs Risk Assessment

## 📋 Opciones de Deployment Gratuitas

### 🥇 **Opción 1: Railway (Recomendado)**

#### **Backend + Base de Datos**
1. Ve a [Railway.app](https://railway.app)
2. Conéctate con GitHub
3. Selecciona "Deploy from GitHub repo"
4. Autoriza Railway y selecciona tu repositorio
5. Railway detectará automáticamente el `Dockerfile`
6. Configura las variables de entorno:
   ```
   PORT=8000
   DATABASE_URL=sqlite:///./database/app.db
   SECRET_KEY=tu-clave-secreta-aqui
   CORS_ORIGINS=https://tu-frontend.vercel.app
   ENVIRONMENT=production
   ```

#### **Frontend en Vercel**
1. Ve a [Vercel.com](https://vercel.com)
2. Importa tu repositorio
3. Configura:
   - Framework: `Vite`
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
4. Variables de entorno:
   ```
   VITE_API_URL=https://tu-backend.railway.app/api/v1
   VITE_BACKEND_URL=https://tu-backend.railway.app
   ```

### 🥈 **Opción 2: Render (Todo en uno)**

#### **Backend**
1. Ve a [Render.com](https://render.com)
2. Conecta GitHub
3. Crea "New Web Service"
4. Configuración:
   - Environment: `Docker`
   - Dockerfile path: `Dockerfile`
   - Port: `8000`

#### **Frontend**
1. Crea "New Static Site"
2. Configuración:
   - Build Command: `cd frontend && npm install && npm run build`
   - Publish Directory: `frontend/dist`

### 🥉 **Opción 3: Supabase + Vercel**

#### **Base de Datos: Supabase**
1. Ve a [Supabase.com](https://supabase.com)
2. Crea nuevo proyecto
3. Obten la URL de conexión PostgreSQL

#### **Backend: Vercel Functions**
1. Modifica el backend para usar Vercel Functions
2. Deploy en Vercel

#### **Frontend: Vercel**
1. Deploy del frontend en Vercel

## 🔧 **Deployment Local con Docker**

```bash
# 1. Build y ejecutar con docker-compose
docker-compose -f docker-compose.prod.yml up --build

# 2. Acceder a la aplicación
# Frontend: http://localhost:80
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## 📝 **Checklist Pre-Deployment**

- [ ] Commit y push todos los cambios a GitHub
- [ ] Verificar que el Dockerfile funciona localmente
- [ ] Configurar variables de entorno de producción
- [ ] Actualizar CORS origins con el dominio del frontend
- [ ] Generar SECRET_KEY segura para producción
- [ ] Probar la aplicación localmente con docker-compose

## 🎯 **URLs de Resultado**

Después del deployment tendrás:
- **Frontend**: `https://tu-proyecto.vercel.app`
- **Backend**: `https://tu-proyecto.railway.app`  
- **API Docs**: `https://tu-proyecto.railway.app/docs`
- **Health Check**: `https://tu-proyecto.railway.app/api/v1/health`

## 💰 **Costos**

- **Railway**: $5/mes gratis, luego $5/mes
- **Vercel**: Gratis para proyectos personales
- **Render**: Gratis con limitaciones
- **Supabase**: 500MB base de datos gratis

## 🔑 **Variables de Entorno Importantes**

### Backend (.env.production)
```
DATABASE_URL=sqlite:///./database/app.db
SECRET_KEY=generate-secure-key-here
CORS_ORIGINS=https://your-frontend-domain.com
ENVIRONMENT=production
PORT=8000
```

### Frontend (.env.production)
```
VITE_API_URL=https://your-backend.railway.app/api/v1
VITE_BACKEND_URL=https://your-backend.railway.app
```

## 🚨 **Troubleshooting**

### Error de CORS
- Actualiza `CORS_ORIGINS` en el backend con la URL del frontend
- Verifica que las URLs no tengan trailing slash

### Error de Base de Datos
- Crea el directorio `database` en Railway
- Verifica permisos de escritura

### Frontend no conecta al Backend
- Verifica las variables `VITE_API_URL` y `VITE_BACKEND_URL`
- Comprueba que el backend esté funcionando

## 📞 **Soporte**

Si tienes problemas:
1. Revisa los logs en Railway/Vercel/Render
2. Verifica que todas las variables de entorno estén configuradas
3. Prueba localmente con Docker primero
