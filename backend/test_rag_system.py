#!/usr/bin/env python3
"""
Test script para verificar el sistema RAG completo
PyMEs Risk Assessment System - The Orellana's Boyz
"""

import requests
import json
import time
from datetime import datetime

# Configuración del servidor
BASE_URL = "http://localhost:8000"

def test_basic_endpoints():
    """Prueba endpoints básicos"""
    print("🔍 Probando endpoints básicos...")
    
    try:
        # Health check
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Health check: {response.status_code}")
        
        # Dashboard
        response = requests.get(f"{BASE_URL}/api/v1/dashboard/summary")
        if response.status_code == 200:
            print(f"✅ Dashboard: {response.json().get('total_applications', 0)} aplicaciones")
        
        # Companies
        response = requests.get(f"{BASE_URL}/api/v1/companies/")
        if response.status_code == 200:
            companies = response.json().get('companies', [])
            print(f"✅ Empresas: {len(companies)} registradas")
            
    except Exception as e:
        print(f"❌ Error en endpoints básicos: {e}")

def test_rag_system_status():
    """Prueba el estado del sistema RAG"""
    print("\n🧠 Verificando sistema RAG...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v2/system/status")
        if response.status_code == 200:
            status = response.json()
            print(f"✅ Sistema RAG: {status.get('system_status', 'unknown')}")
            
            components = status.get('components', {})
            print(f"  📊 ChromaDB: {components.get('chromadb', {}).get('status', 'unknown')}")
            print(f"  🤖 Gemini LLM: {components.get('gemini_llm', {}).get('status', 'unknown')}")
            print(f"  🕸️  Web Scraper: {components.get('web_scraper', {}).get('status', 'unknown')}")
            
            capabilities = status.get('capabilities', [])
            print(f"  💡 Capacidades: {len(capabilities)} disponibles")
            
        else:
            print(f"❌ Error obteniendo estado RAG: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error verificando RAG: {e}")

def test_document_upload():
    """Prueba carga de documentos"""
    print("\n📄 Probando carga de documentos...")
    
    try:
        # Documento financiero simulado
        test_document = {
            "company_ruc": "1234567890001",
            "document_content": """
            ESTADO FINANCIERO - TECHSTART ECUADOR S.A.
            
            BALANCE GENERAL 2024:
            Activos Corrientes: $250,000
            - Efectivo y Equivalentes: $80,000
            - Cuentas por Cobrar: $120,000
            - Inventarios: $50,000
            
            Activos No Corrientes: $350,000
            - Propiedad, Planta y Equipo: $300,000
            - Activos Intangibles: $50,000
            
            PASIVOS:
            Pasivos Corrientes: $150,000
            - Cuentas por Pagar: $100,000
            - Deuda a Corto Plazo: $50,000
            
            Pasivos No Corrientes: $200,000
            - Deuda a Largo Plazo: $200,000
            
            PATRIMONIO: $250,000
            
            ESTADO DE RESULTADOS 2024:
            Ingresos: $500,000
            Costo de Ventas: $300,000
            Utilidad Bruta: $200,000
            Gastos Operativos: $150,000
            EBITDA: $50,000
            Utilidad Neta: $35,000
            
            INDICADORES FINANCIEROS:
            - Liquidez Corriente: 1.67
            - Rotación de Inventarios: 6.0
            - Margen Bruto: 40%
            - ROE: 14%
            - Endeudamiento: 58%
            """,
            "document_type": "financial_statement"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/v2/documents/upload",
            json=test_document
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Documento cargado: {result.get('chunks_processed', 0)} chunks procesados")
            print(f"  📝 ID del documento: {result.get('document_id', 'N/A')}")
        else:
            print(f"❌ Error cargando documento: {response.status_code}")
            print(f"  Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error en carga de documento: {e}")

def test_sentiment_analysis():
    """Prueba análisis de sentimiento"""
    print("\n📱 Probando análisis de sentimiento...")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v2/sentiment/1234567890001",
            params={"company_name": "TechStart Ecuador S.A."}
        )
        
        if response.status_code == 200:
            sentiment = response.json()
            social_data = sentiment.get('sentiment_analysis', {}).get('social_media', {})
            sentiment_dist = social_data.get('sentiment_distribution', {})
            
            print(f"✅ Sentimiento analizado:")
            print(f"  👥 Menciones totales: {social_data.get('total_mentions', 0)}")
            print(f"  😊 Positivo: {sentiment_dist.get('positive', 0):.2%}")
            print(f"  😐 Neutral: {sentiment_dist.get('neutral', 0):.2%}")
            print(f"  😞 Negativo: {sentiment_dist.get('negative', 0):.2%}")
        else:
            print(f"❌ Error en análisis de sentimiento: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error en sentimiento: {e}")

def test_comprehensive_analysis():
    """Prueba análisis completo RAG"""
    print("\n🎯 Probando análisis RAG completo...")
    
    try:
        analysis_request = {
            "company_ruc": "1234567890001",
            "company_name": "TechStart Ecuador S.A.",
            "sector": "Tecnología",
            "financial_documents": [
                "Estado financiero mostrando ingresos de $500,000 y utilidad neta de $35,000"
            ],
            "include_market_analysis": True
        }
        
        response = requests.post(
            f"{BASE_URL}/api/v2/analysis/comprehensive",
            json=analysis_request
        )
        
        if response.status_code == 200:
            analysis = response.json()
            risk_data = analysis.get('risk_assessment', {})
            
            print(f"✅ Análisis RAG completado:")
            print(f"  🎯 Score de riesgo: {risk_data.get('final_risk_score', 0):.2f}")
            print(f"  📊 Nivel de riesgo: {risk_data.get('risk_level', 'unknown')}")
            print(f"  💡 Recomendación: {risk_data.get('recommendation', 'N/A')}")
            
            detailed = risk_data.get('detailed_analysis', {})
            print(f"  📈 Score financiero base: {detailed.get('base_financial_score', 0):.2f}")
            print(f"  📱 Score sentimiento: {detailed.get('market_sentiment_score', 0):.2f}")
            print(f"  🤖 Score LLM: {detailed.get('llm_analysis_score', 0):.2f}")
            print(f"  📄 Documentos de apoyo: {risk_data.get('supporting_documents', 0)}")
            
        else:
            print(f"❌ Error en análisis RAG: {response.status_code}")
            print(f"  Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error en análisis completo: {e}")

def test_semantic_search():
    """Prueba búsqueda semántica"""
    print("\n🔍 Probando búsqueda semántica...")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v2/documents/search",
            params={
                "query": "indicadores financieros liquidez",
                "company_ruc": "1234567890001",
                "limit": 3
            }
        )
        
        if response.status_code == 200:
            search_result = response.json()
            docs_found = search_result.get('documents_found', 0)
            relevant_docs = search_result.get('relevant_documents', [])
            
            print(f"✅ Búsqueda semántica:")
            print(f"  📋 Documentos encontrados: {docs_found}")
            
            for i, doc in enumerate(relevant_docs[:2]):
                content_preview = doc.get('content', '')[:100] + "..."
                print(f"  📄 Doc {i+1}: {content_preview}")
                
        else:
            print(f"❌ Error en búsqueda semántica: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error en búsqueda: {e}")

def test_sector_analysis():
    """Prueba análisis sectorial"""
    print("\n📈 Probando análisis sectorial...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v2/sector/analysis/Tecnología")
        
        if response.status_code == 200:
            sector_data = response.json()
            risk_stats = sector_data.get('risk_statistics', {})
            
            print(f"✅ Análisis sectorial - Tecnología:")
            print(f"  🏢 Empresas analizadas: {sector_data.get('companies_analyzed', 0)}")
            print(f"  📊 Riesgo promedio: {risk_stats.get('average_risk_score', 0):.2f}")
            print(f"  📈 Distribución de riesgo:")
            
            distribution = risk_stats.get('risk_distribution', {})
            print(f"    🟢 Bajo riesgo: {distribution.get('low_risk', 0)}")
            print(f"    🟡 Riesgo medio: {distribution.get('medium_risk', 0)}")
            print(f"    🔴 Alto riesgo: {distribution.get('high_risk', 0)}")
            
            insights = sector_data.get('sector_insights', {})
            print(f"  💹 Tendencia de crecimiento: {insights.get('growth_trend', 'unknown')}")
            print(f"  💰 Límite recomendado: ${insights.get('recommended_credit_limit', 0):,}")
            
        else:
            print(f"❌ Error en análisis sectorial: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error en análisis sectorial: {e}")

def test_llm_direct():
    """Prueba análisis LLM directo"""
    print("\n🤖 Probando análisis LLM directo...")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v2/llm/analyze",
            params={
                "company_name": "TechStart Ecuador S.A.",
                "company_ruc": "1234567890001",
                "sector": "Tecnología",
                "include_context": "true"
            }
        )
        
        if response.status_code == 200:
            llm_result = response.json()
            llm_analysis = llm_result.get('llm_analysis', {})
            
            if llm_analysis.get('success'):
                analysis_data = llm_analysis.get('llm_analysis', {})
                print(f"✅ Análisis LLM completado:")
                print(f"  🎯 Score de riesgo: {analysis_data.get('risk_score', 'N/A')}")
                print(f"  📊 Nivel de riesgo: {analysis_data.get('risk_level', 'N/A')}")
                print(f"  🎯 Confianza: {analysis_data.get('confidence_level', 'N/A')}")
                print(f"  📝 Resumen: {analysis_data.get('executive_summary', 'N/A')[:100]}...")
            else:
                print(f"⚠️  LLM Analysis falló: {llm_analysis.get('error', 'Unknown error')}")
                
        else:
            print(f"❌ Error en análisis LLM: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error en LLM directo: {e}")

def main():
    """Ejecuta todas las pruebas"""
    print("🚀 SISTEMA DE PRUEBAS RAG - PyMEs Risk Assessment")
    print("=" * 60)
    print(f"📍 URL del servidor: {BASE_URL}")
    print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Verificar que el servidor esté corriendo
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor conectado correctamente")
        else:
            print(f"⚠️  Servidor responde con código: {response.status_code}")
    except Exception as e:
        print(f"❌ Error conectando al servidor: {e}")
        print("🔧 Asegúrate de que el servidor esté corriendo en el puerto 8000")
        return
    
    # Ejecutar pruebas
    test_basic_endpoints()
    time.sleep(1)
    
    test_rag_system_status()
    time.sleep(1)
    
    test_document_upload()
    time.sleep(2)  # Dar tiempo para que se procese el documento
    
    test_sentiment_analysis()
    time.sleep(1)
    
    test_semantic_search()
    time.sleep(1)
    
    test_comprehensive_analysis()
    time.sleep(1)
    
    test_sector_analysis()
    time.sleep(1)
    
    test_llm_direct()
    
    print("\n" + "=" * 60)
    print("🎉 PRUEBAS COMPLETADAS")
    print("💡 Revisa los resultados arriba para verificar el funcionamiento")
    print("📚 Para más detalles, visita: http://localhost:8000/docs")
    print("=" * 60)

if __name__ == "__main__":
    main()
