#!/usr/bin/env python3
"""
🏆 ARCHIVO DE PRUEBAS PARA EL HACKATHON VIAMATICA
Reto 2: Evaluación Inteligente de Riesgo Financiero para PYMEs

Este archivo contiene pruebas específicas para los nuevos endpoints
desarrollados para el hackathon.

Team: The Orellana's Boyz
"""

import requests
import json
import time
from typing import Dict, Any

class HackathonAPITester:
    """Clase para probar los endpoints del hackathon"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def test_system_status(self) -> Dict[str, Any]:
        """Probar estado del sistema"""
        print("🟢 Probando estado del sistema RAG...")
        
        response = self.session.get(f"{self.base_url}/api/v2/system/status")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Sistema RAG funcional:")
            print(f"   📊 ChromaDB: {'✅' if data.get('chromadb_status') else '❌'}")
            print(f"   🤖 Gemini LLM: {'✅' if data.get('llm_status') else '❌'}")
            print(f"   💾 Base de datos: {'✅' if data.get('database_status') else '❌'}")
            return data
        else:
            print(f"❌ Error en estado del sistema: {response.status_code}")
            return {}
    
    def test_demo_data(self) -> Dict[str, Any]:
        """Probar endpoint de datos de demostración"""
        print("\n🎯 Probando datos de demostración...")
        
        response = self.session.get(f"{self.base_url}/api/v2/hackathon/demo-data")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Datos de demo disponibles:")
            print(f"   🏢 Empresas demo: {len(data.get('demo_companies', []))}")
            print(f"   📄 Documentos demo: {len(data.get('sample_documents', []))}")
            print(f"   📈 Escenarios demo: {len(data.get('demo_scenarios', []))}")
            
            for company in data.get('demo_companies', [])[:2]:
                print(f"   📋 {company['name']} - {company['sector']}")
            
            return data
        else:
            print(f"❌ Error obteniendo datos demo: {response.status_code}")
            return {}
    
    def test_company_search(self, ruc: str = "1791234567001") -> Dict[str, Any]:
        """Probar búsqueda en Super de Compañías"""
        print(f"\n🔍 Probando búsqueda de empresa RUC: {ruc}...")
        
        response = self.session.get(f"{self.base_url}/api/v2/hackathon/company-search/{ruc}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('found'):
                print(f"✅ Empresa encontrada en SCVS:")
                company_data = data.get('company_data', {})
                print(f"   🏢 Nombre: {company_data.get('company_name', 'N/A')}")
                print(f"   📊 Estado: {company_data.get('status', 'N/A')}")
                print(f"   📅 Constitución: {company_data.get('constitution_date', 'N/A')}")
            else:
                print(f"⚠️ Empresa no encontrada en base de datos SCVS")
            return data
        else:
            print(f"❌ Error en búsqueda: {response.status_code}")
            return {}
    
    def test_digital_footprint_analysis(self, company_name: str = "TechStart Ecuador", 
                                      company_ruc: str = "1791234567001") -> Dict[str, Any]:
        """Probar análisis de huella digital"""
        print(f"\n🌐 Probando análisis de huella digital para: {company_name}...")
        
        data = {
            "company_name": company_name,
            "company_ruc": company_ruc,
            "social_media_urls": "https://facebook.com/techstart,https://linkedin.com/company/techstart"
        }
        
        response = self.session.post(
            f"{self.base_url}/api/v2/hackathon/digital-footprint-analysis",
            data=data
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Análisis digital completado:")
            
            digital_analysis = result.get('digital_analysis', {})
            digital_score = digital_analysis.get('digital_score', {})
            
            print(f"   📊 Score digital: {digital_score.get('overall_digital_score', 'N/A')}/100")
            print(f"   🌐 Presencia web: {'✅' if digital_analysis.get('web_presence') else '❌'}")
            print(f"   📱 Redes sociales: {len(digital_analysis.get('social_media_analysis', {}).get('platforms', []))}")
            
            return result
        else:
            print(f"❌ Error en análisis digital: {response.status_code}")
            return {}
    
    def test_scenario_simulations(self, company_name: str = "TechStart Ecuador",
                                company_ruc: str = "1791234567001") -> Dict[str, Any]:
        """Probar simulaciones de escenarios"""
        print(f"\n📈 Probando simulaciones de escenarios para: {company_name}...")
        
        data = {
            "company_ruc": company_ruc,
            "company_name": company_name,
            "sector": "Tecnología",
            "current_revenue": 500000,
            "current_risk_score": 65
        }
        
        response = self.session.post(
            f"{self.base_url}/api/v2/hackathon/scenario-simulations",
            data=data
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Simulaciones generadas:")
            
            simulations = result.get('simulations', {})
            scenarios = simulations.get('scenarios', {})
            
            print(f"   📊 Escenarios generados: {len(scenarios)}")
            
            for scenario_type, scenario_data in scenarios.items():
                if isinstance(scenario_data, dict):
                    print(f"   🎯 {scenario_type}: {scenario_data.get('description', 'N/A')}")
            
            return result
        else:
            print(f"❌ Error en simulaciones: {response.status_code}")
            return {}
    
    def test_comprehensive_analysis(self, company_ruc: str = "1791234567001",
                                  company_name: str = "TechStart Ecuador") -> Dict[str, Any]:
        """Probar análisis comprehensivo - ENDPOINT PRINCIPAL"""
        print(f"\n🎯 PROBANDO ANÁLISIS INTEGRAL HACKATHON...")
        print(f"   🏢 Empresa: {company_name}")
        print(f"   🆔 RUC: {company_ruc}")
        
        data = {
            "company_ruc": company_ruc,
            "company_name": company_name,
            "sector": "Tecnología",
            "social_media_urls": [
                "https://facebook.com/techstartec",
                "https://linkedin.com/company/techstart"
            ],
            "include_supercias_data": True,
            "include_digital_footprint": True,
            "include_scenario_analysis": True
        }
        
        print("⏳ Ejecutando análisis (puede tomar 30-60 segundos)...")
        start_time = time.time()
        
        response = self.session.post(
            f"{self.base_url}/api/v2/hackathon/comprehensive-analysis",
            json=data,
            timeout=120  # 2 minutos timeout
        )
        
        processing_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ ANÁLISIS INTEGRAL COMPLETADO en {processing_time:.1f}s")
            
            analysis_result = result.get('analysis_result', {})
            integrated_assessment = analysis_result.get('integrated_risk_assessment', {})
            hackathon_score = analysis_result.get('hackathon_score', {})
            
            print(f"\\n🏆 RESULTADOS FINALES:")
            print(f"   📊 Score Final: {hackathon_score.get('score', 'N/A')}/100")
            print(f"   🎯 Clasificación: {hackathon_score.get('classification', 'N/A')}")
            print(f"   ⚖️ Recomendación: {integrated_assessment.get('recommendation', 'N/A')}")
            print(f"   🔍 Confianza: {integrated_assessment.get('confidence_level', 'N/A')}")
            
            # Mostrar componentes analizados
            analysis_components = analysis_result.get('analysis_components', {})
            print(f"\\n📋 COMPONENTES ANALIZADOS:")
            
            if analysis_components.get('supercias_data'):
                print(f"   ✅ Datos Super de Compañías")
            if analysis_components.get('digital_footprint'):
                print(f"   ✅ Huella Digital")
            if analysis_components.get('scenario_simulations'):
                print(f"   ✅ Simulaciones de Escenarios")
            if analysis_components.get('rag_analysis'):
                print(f"   ✅ Análisis RAG")
            
            # Mostrar recomendaciones
            recommendations = analysis_result.get('recommendations', [])
            if recommendations:
                print(f"\\n💡 RECOMENDACIONES:")
                for i, rec in enumerate(recommendations[:3], 1):
                    print(f"   {i}. {rec}")
            
            return result
        else:
            print(f"❌ Error en análisis integral: {response.status_code}")
            try:
                error_detail = response.json()
                print(f"   Detalle: {error_detail.get('detail', 'Error desconocido')}")
            except:
                print(f"   Respuesta: {response.text[:200]}...")
            return {}
    
    def run_full_test_suite(self):
        """Ejecutar suite completa de pruebas"""
        print("🚀 INICIANDO SUITE DE PRUEBAS HACKATHON VIAMATICA")
        print("=" * 60)
        
        # Test 1: Sistema
        self.test_system_status()
        
        # Test 2: Datos demo
        demo_data = self.test_demo_data()
        
        # Test 3: Usar empresa de demo si está disponible
        test_company_ruc = "1791234567001"
        test_company_name = "TechStart Ecuador S.A."
        
        if demo_data and demo_data.get('demo_companies'):
            demo_company = demo_data['demo_companies'][0]
            test_company_ruc = demo_company['ruc']
            test_company_name = demo_company['name']
        
        # Test 4: Búsqueda empresa
        self.test_company_search(test_company_ruc)
        
        # Test 5: Análisis digital
        self.test_digital_footprint_analysis(test_company_name, test_company_ruc)
        
        # Test 6: Simulaciones
        self.test_scenario_simulations(test_company_name, test_company_ruc)
        
        # Test 7: Análisis integral (PRINCIPAL)
        self.test_comprehensive_analysis(test_company_ruc, test_company_name)
        
        print("\\n" + "=" * 60)
        print("🎉 SUITE DE PRUEBAS COMPLETADA")
        print("🏆 Sistema listo para demostración del hackathon")

def main():
    """Función principal para ejecutar las pruebas"""
    print("🏆 HACKATHON VIAMATICA - PRUEBAS DE ENDPOINTS")
    print("Reto 2: Evaluación Inteligente de Riesgo Financiero para PYMEs")
    print("Team: The Orellana's Boyz")
    print("\\n")
    
    # Crear instancia del tester
    tester = HackathonAPITester()
    
    try:
        # Verificar que el servidor esté corriendo
        response = requests.get(f"{tester.base_url}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor detectado y corriendo")
            print(f"📖 Documentación disponible en: {tester.base_url}/docs")
            print("\\n")
            
            # Ejecutar suite completa
            tester.run_full_test_suite()
            
        else:
            print(f"❌ Servidor no responde correctamente (status: {response.status_code})")
            
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor")
        print("💡 Asegúrate de que el backend esté corriendo en http://localhost:8000")
        print("   Ejecuta: python main_production.py")
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()
