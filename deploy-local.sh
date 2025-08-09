#!/bin/bash

echo "🚀 Iniciando deployment local con Docker..."
echo

# Verificar que Docker esté ejecutándose
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado"
    echo "📝 Instala Docker desde https://docker.com"
    exit 1
fi

if ! docker info &> /dev/null; then
    echo "❌ Docker no está ejecutándose"
    echo "📝 Asegúrate de que Docker Desktop esté ejecutándose"
    exit 1
fi

echo "✅ Docker está funcionando"
echo

echo "📦 Construyendo imágenes Docker..."
docker-compose -f docker-compose.prod.yml build

if [ $? -ne 0 ]; then
    echo "❌ Error construyendo las imágenes"
    exit 1
fi

echo "✅ Imágenes construidas exitosamente"
echo

echo "🚀 Iniciando contenedores..."
docker-compose -f docker-compose.prod.yml up -d

if [ $? -ne 0 ]; then
    echo "❌ Error iniciando los contenedores"
    exit 1
fi

echo "✅ Contenedores iniciados exitosamente"
echo
echo "🌐 URLs disponibles:"
echo "   Frontend: http://localhost:80"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo
echo "📝 Para ver los logs: docker-compose -f docker-compose.prod.yml logs -f"
echo "📝 Para parar: docker-compose -f docker-compose.prod.yml down"
echo
