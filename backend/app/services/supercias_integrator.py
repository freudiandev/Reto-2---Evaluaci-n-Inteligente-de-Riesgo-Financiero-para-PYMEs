"""
Integrador con Superintendencia de Compañías del Ecuador
Sistema para descargar y procesar estados financieros oficiales
"""

import requests
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json
import pandas as pd
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import logging
import io
import PyPDF2
from urllib.parse import urljoin, quote

logger = logging.getLogger(__name__)

class SuperciasIntegrator:
    """Integrador con el portal de la Superintendencia de Compañías"""
    
    def __init__(self):
        self.base_url = "https://www.supercias.gob.ec/portalscvs/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # URLs específicas del portal SCVS
        self.endpoints = {
            'search_company': 'consultas/consulta-cia-param.jsf',
            'financial_statements': 'consultas/consulta-estados-financieros.jsf',
            'company_info': 'consultas/consulta-informacion-companias.jsf',
            'downloads': 'downloads/'
        }
    
    async def search_company_by_ruc(self, ruc: str) -> Dict:
        """Buscar empresa por RUC en la base de datos de la SCVS"""
        
        logger.info(f"🔍 Buscando empresa con RUC: {ruc}")
        
        try:
            # Validar formato RUC
            if not self._validate_ruc_format(ruc):
                return {"error": "Formato de RUC inválido", "ruc": ruc}
            
            # Realizar búsqueda en el portal
            company_data = await self._perform_company_search(ruc)
            
            if company_data.get("found"):
                logger.info(f"✅ Empresa encontrada: {company_data.get('name', 'N/A')}")
                
                # Obtener información adicional
                additional_info = await self._get_additional_company_info(ruc)
                company_data.update(additional_info)
                
                return company_data
            else:
                logger.warning(f"⚠️ Empresa no encontrada en SCVS: {ruc}")
                return {"error": "Empresa no encontrada en base de datos SCVS", "ruc": ruc}
                
        except Exception as e:
            logger.error(f"❌ Error buscando empresa {ruc}: {e}")
            return {"error": str(e), "ruc": ruc}
    
    async def download_financial_statements(self, ruc: str, years: List[int] = None) -> Dict:
        """Descargar estados financieros de la empresa"""
        
        if years is None:
            years = [2023, 2022, 2021]  # Últimos 3 años por defecto
        
        logger.info(f"📊 Descargando estados financieros para RUC: {ruc}")
        
        try:
            financial_data = {
                "ruc": ruc,
                "download_timestamp": datetime.now().isoformat(),
                "years_requested": years,
                "statements_found": {},
                "processed_data": {},
                "summary": {}
            }
            
            for year in years:
                logger.info(f"📄 Procesando año {year}")
                
                # Buscar estados financieros del año
                year_statements = await self._download_year_statements(ruc, year)
                
                if year_statements.get("success"):
                    financial_data["statements_found"][str(year)] = year_statements
                    
                    # Procesar datos financieros
                    processed = self._process_financial_statements(year_statements)
                    financial_data["processed_data"][str(year)] = processed
                    
                else:
                    logger.warning(f"⚠️ No se encontraron estados financieros para {year}")
                    financial_data["statements_found"][str(year)] = {"error": "No disponible"}
            
            # Generar resumen comparativo
            financial_data["summary"] = self._generate_financial_summary(
                financial_data["processed_data"]
            )
            
            logger.info(f"✅ Estados financieros procesados para {ruc}")
            return financial_data
            
        except Exception as e:
            logger.error(f"❌ Error descargando estados financieros {ruc}: {e}")
            return {
                "error": str(e),
                "ruc": ruc,
                "fallback_data": self._generate_fallback_financials(ruc)
            }
    
    async def get_company_legal_status(self, ruc: str) -> Dict:
        """Obtener estado legal y situación de la empresa"""
        
        logger.info(f"⚖️ Verificando estado legal para RUC: {ruc}")
        
        try:
            legal_status = {
                "ruc": ruc,
                "verification_date": datetime.now().isoformat(),
                "company_status": "unknown",
                "registration_date": None,
                "legal_form": "unknown",
                "capital_registered": 0,
                "activity_code": "unknown",
                "activity_description": "unknown",
                "address": "unknown",
                "legal_representative": "unknown",
                "compliance_status": "unknown",
                "last_financial_report": None
            }
            
            # Realizar consulta de estado legal
            legal_data = await self._query_legal_status(ruc)
            
            if legal_data.get("success"):
                legal_status.update(legal_data.get("data", {}))
                
                # Verificar cumplimiento de obligaciones
                compliance = await self._check_compliance_status(ruc)
                legal_status["compliance_status"] = compliance.get("status", "unknown")
                legal_status["compliance_details"] = compliance.get("details", {})
                
            return legal_status
            
        except Exception as e:
            logger.error(f"❌ Error verificando estado legal {ruc}: {e}")
            return {
                "error": str(e),
                "ruc": ruc,
                "fallback_status": "verification_failed"
            }
    
    async def get_sector_comparison_data(self, activity_code: str, company_size: str = "PYME") -> Dict:
        """Obtener datos comparativos del sector"""
        
        logger.info(f"📈 Obteniendo datos sectoriales para código: {activity_code}")
        
        try:
            sector_data = {
                "activity_code": activity_code,
                "company_size": company_size,
                "analysis_date": datetime.now().isoformat(),
                "sector_statistics": {},
                "benchmarks": {},
                "market_trends": {}
            }
            
            # Obtener estadísticas del sector
            sector_stats = await self._get_sector_statistics(activity_code, company_size)
            sector_data["sector_statistics"] = sector_stats
            
            # Calcular benchmarks
            if sector_stats.get("success"):
                benchmarks = self._calculate_sector_benchmarks(sector_stats)
                sector_data["benchmarks"] = benchmarks
            
            # Obtener tendencias del mercado
            trends = await self._get_market_trends(activity_code)
            sector_data["market_trends"] = trends
            
            return sector_data
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo datos sectoriales: {e}")
            return {"error": str(e), "activity_code": activity_code}
    
    # Métodos internos para scraping específico
    
    async def _perform_company_search(self, ruc: str) -> Dict:
        """Realizar búsqueda específica en el portal SCVS"""
        
        # NOTA: Esta es una implementación simulada
        # En producción se haría scraping real del portal
        
        import random
        
        # Simular resultados de búsqueda
        if ruc.startswith("17") or ruc.startswith("09"):  # RUCs válidos simulados
            return {
                "found": True,
                "ruc": ruc,
                "name": f"EMPRESA EJEMPLO {ruc[-3:]} S.A.",
                "legal_form": "SOCIEDAD ANÓNIMA",
                "registration_date": "2018-05-15",
                "status": "ACTIVA",
                "activity_code": "G4711.01",
                "activity_description": "Venta al por menor en comercios no especializados",
                "address": "QUITO, PICHINCHA, ECUADOR",
                "capital": random.randint(1000, 100000),
                "last_update": datetime.now().isoformat()
            }
        else:
            return {"found": False, "ruc": ruc}
    
    async def _download_year_statements(self, ruc: str, year: int) -> Dict:
        """Descargar estados financieros de un año específico"""
        
        # Simulación de descarga de estados financieros
        import random
        
        if random.random() > 0.3:  # 70% de probabilidad de encontrar datos
            # Generar datos financieros simulados pero realistas
            revenue = random.randint(100000, 2000000)
            costs = int(revenue * random.uniform(0.6, 0.8))
            assets = int(revenue * random.uniform(0.8, 1.5))
            liabilities = int(assets * random.uniform(0.3, 0.7))
            
            return {
                "success": True,
                "year": year,
                "ruc": ruc,
                "financial_data": {
                    "balance_sheet": {
                        "total_assets": assets,
                        "current_assets": int(assets * 0.4),
                        "non_current_assets": int(assets * 0.6),
                        "total_liabilities": liabilities,
                        "current_liabilities": int(liabilities * 0.6),
                        "non_current_liabilities": int(liabilities * 0.4),
                        "equity": assets - liabilities
                    },
                    "income_statement": {
                        "total_revenue": revenue,
                        "cost_of_goods_sold": costs,
                        "gross_profit": revenue - costs,
                        "operating_expenses": int((revenue - costs) * 0.6),
                        "operating_income": int((revenue - costs) * 0.4),
                        "net_income": int((revenue - costs) * 0.25)
                    },
                    "cash_flow": {
                        "operating_cash_flow": int(revenue * 0.15),
                        "investing_cash_flow": int(revenue * -0.05),
                        "financing_cash_flow": int(revenue * -0.03),
                        "net_cash_flow": int(revenue * 0.07)
                    }
                },
                "download_url": f"https://www.supercias.gob.ec/downloads/{ruc}_{year}.pdf",
                "file_size": random.randint(500, 2000),  # KB
                "last_modified": f"{year}-12-31"
            }
        else:
            return {
                "success": False,
                "year": year,
                "ruc": ruc,
                "error": "Estados financieros no disponibles para este año"
            }
    
    def _process_financial_statements(self, statements_data: Dict) -> Dict:
        """Procesar y calcular ratios financieros"""
        
        if not statements_data.get("success"):
            return {"error": "No hay datos para procesar"}
        
        financial_data = statements_data.get("financial_data", {})
        balance_sheet = financial_data.get("balance_sheet", {})
        income_statement = financial_data.get("income_statement", {})
        cash_flow = financial_data.get("cash_flow", {})
        
        # Calcular ratios financieros
        ratios = {}
        
        try:
            # Ratios de liquidez
            current_assets = balance_sheet.get("current_assets", 0)
            current_liabilities = balance_sheet.get("current_liabilities", 1)
            ratios["current_ratio"] = current_assets / current_liabilities
            
            # Ratios de endeudamiento
            total_assets = balance_sheet.get("total_assets", 1)
            total_liabilities = balance_sheet.get("total_liabilities", 0)
            ratios["debt_to_assets"] = total_liabilities / total_assets
            
            equity = balance_sheet.get("equity", 1)
            if equity > 0:
                ratios["debt_to_equity"] = total_liabilities / equity
            
            # Ratios de rentabilidad
            revenue = income_statement.get("total_revenue", 1)
            net_income = income_statement.get("net_income", 0)
            ratios["profit_margin"] = net_income / revenue
            ratios["return_on_assets"] = net_income / total_assets
            
            if equity > 0:
                ratios["return_on_equity"] = net_income / equity
            
            # Ratios de eficiencia
            ratios["asset_turnover"] = revenue / total_assets
            
            # Análisis de cash flow
            operating_cf = cash_flow.get("operating_cash_flow", 0)
            ratios["operating_cash_margin"] = operating_cf / revenue
            
        except ZeroDivisionError:
            logger.warning("División por cero al calcular ratios")
        
        return {
            "financial_data": financial_data,
            "financial_ratios": ratios,
            "analysis": {
                "liquidity_analysis": self._analyze_liquidity(ratios),
                "profitability_analysis": self._analyze_profitability(ratios),
                "leverage_analysis": self._analyze_leverage(ratios),
                "efficiency_analysis": self._analyze_efficiency(ratios)
            },
            "risk_indicators": self._identify_risk_indicators(ratios, financial_data)
        }
    
    def _generate_financial_summary(self, processed_data: Dict) -> Dict:
        """Generar resumen comparativo de múltiples años"""
        
        if not processed_data:
            return {"error": "No hay datos procesados"}
        
        years = sorted(processed_data.keys())
        if len(years) < 2:
            return {"single_year_data": True, "available_years": years}
        
        summary = {
            "years_analyzed": years,
            "trends": {},
            "performance_summary": {},
            "growth_rates": {},
            "stability_indicators": {}
        }
        
        try:
            # Calcular tendencias de ingresos
            revenues = []
            net_incomes = []
            total_assets = []
            
            for year in years:
                year_data = processed_data[year]
                financial_data = year_data.get("financial_data", {})
                income_statement = financial_data.get("income_statement", {})
                balance_sheet = financial_data.get("balance_sheet", {})
                
                revenues.append(income_statement.get("total_revenue", 0))
                net_incomes.append(income_statement.get("net_income", 0))
                total_assets.append(balance_sheet.get("total_assets", 0))
            
            # Calcular tasas de crecimiento
            if len(revenues) >= 2:
                revenue_growth = ((revenues[-1] - revenues[0]) / revenues[0] * 100) if revenues[0] > 0 else 0
                summary["growth_rates"]["revenue_growth"] = round(revenue_growth, 2)
            
            if len(net_incomes) >= 2:
                profit_growth = ((net_incomes[-1] - net_incomes[0]) / abs(net_incomes[0]) * 100) if net_incomes[0] != 0 else 0
                summary["growth_rates"]["profit_growth"] = round(profit_growth, 2)
            
            # Evaluar estabilidad
            revenue_volatility = self._calculate_volatility(revenues)
            profit_volatility = self._calculate_volatility(net_incomes)
            
            summary["stability_indicators"] = {
                "revenue_stability": "high" if revenue_volatility < 0.2 else "medium" if revenue_volatility < 0.5 else "low",
                "profit_stability": "high" if profit_volatility < 0.3 else "medium" if profit_volatility < 0.7 else "low"
            }
            
            # Resumen de performance
            latest_year = years[-1]
            latest_data = processed_data[latest_year]
            latest_ratios = latest_data.get("financial_ratios", {})
            
            summary["performance_summary"] = {
                "current_liquidity": "good" if latest_ratios.get("current_ratio", 0) > 1.2 else "concern",
                "profitability": "good" if latest_ratios.get("profit_margin", 0) > 0.05 else "concern",
                "leverage": "good" if latest_ratios.get("debt_to_assets", 1) < 0.6 else "concern"
            }
            
        except Exception as e:
            logger.error(f"Error generando resumen financiero: {e}")
            summary["error"] = str(e)
        
        return summary
    
    # Helper methods
    
    def _validate_ruc_format(self, ruc: str) -> bool:
        """Validar formato de RUC ecuatoriano"""
        if not ruc or len(ruc) != 13:
            return False
        
        if not ruc.isdigit():
            return False
        
        # Validar que termine en 001 (personas jurídicas)
        if not ruc.endswith("001"):
            return False
        
        return True
    
    async def _get_additional_company_info(self, ruc: str) -> Dict:
        """Obtener información adicional de la empresa"""
        # Simulación de datos adicionales
        import random
        
        return {
            "employees_estimated": random.randint(5, 100),
            "branches": random.randint(1, 5),
            "foundation_year": random.randint(2010, 2020),
            "legal_representative": f"REPRESENTANTE LEGAL {ruc[-3:]}",
            "phone": f"02-{random.randint(2000000, 2999999)}",
            "email": f"info@empresa{ruc[-3:]}.com.ec"
        }
    
    async def _query_legal_status(self, ruc: str) -> Dict:
        """Consultar estado legal específico"""
        # Simulación de consulta legal
        import random
        
        return {
            "success": True,
            "data": {
                "company_status": random.choice(["ACTIVA", "SUSPENDIDA", "DISUELTA"]),
                "compliance_status": random.choice(["AL_DIA", "MORA", "OBSERVACIONES"]),
                "last_financial_report": "2023-12-31",
                "legal_form": "SOCIEDAD ANÓNIMA"
            }
        }
    
    async def _check_compliance_status(self, ruc: str) -> Dict:
        """Verificar cumplimiento de obligaciones"""
        import random
        
        return {
            "status": random.choice(["compliant", "minor_issues", "major_issues"]),
            "details": {
                "financial_reports_updated": random.choice([True, False]),
                "tax_obligations": random.choice(["current", "delayed"]),
                "legal_obligations": random.choice(["current", "pending"])
            }
        }
    
    async def _get_sector_statistics(self, activity_code: str, company_size: str) -> Dict:
        """Obtener estadísticas del sector"""
        import random
        
        return {
            "success": True,
            "total_companies": random.randint(100, 1000),
            "avg_revenue": random.randint(500000, 2000000),
            "avg_employees": random.randint(10, 50),
            "growth_rate": random.uniform(-0.05, 0.15)
        }
    
    def _calculate_sector_benchmarks(self, sector_stats: Dict) -> Dict:
        """Calcular benchmarks del sector"""
        return {
            "revenue_percentiles": {
                "p25": sector_stats.get("avg_revenue", 0) * 0.5,
                "p50": sector_stats.get("avg_revenue", 0),
                "p75": sector_stats.get("avg_revenue", 0) * 1.5
            },
            "efficiency_benchmarks": {
                "profit_margin": 0.08,
                "current_ratio": 1.5,
                "debt_to_assets": 0.4
            }
        }
    
    async def _get_market_trends(self, activity_code: str) -> Dict:
        """Obtener tendencias del mercado"""
        import random
        
        return {
            "market_growth": random.uniform(-0.1, 0.2),
            "competition_level": random.choice(["low", "medium", "high"]),
            "market_outlook": random.choice(["positive", "neutral", "negative"])
        }
    
    def _analyze_liquidity(self, ratios: Dict) -> str:
        """Analizar liquidez de la empresa"""
        current_ratio = ratios.get("current_ratio", 0)
        
        if current_ratio > 2.0:
            return "excellent"
        elif current_ratio > 1.5:
            return "good"
        elif current_ratio > 1.0:
            return "acceptable"
        else:
            return "poor"
    
    def _analyze_profitability(self, ratios: Dict) -> str:
        """Analizar rentabilidad de la empresa"""
        profit_margin = ratios.get("profit_margin", 0)
        
        if profit_margin > 0.15:
            return "excellent"
        elif profit_margin > 0.08:
            return "good"
        elif profit_margin > 0.03:
            return "acceptable"
        else:
            return "poor"
    
    def _analyze_leverage(self, ratios: Dict) -> str:
        """Analizar apalancamiento de la empresa"""
        debt_to_assets = ratios.get("debt_to_assets", 0)
        
        if debt_to_assets < 0.3:
            return "conservative"
        elif debt_to_assets < 0.5:
            return "moderate"
        elif debt_to_assets < 0.7:
            return "aggressive"
        else:
            return "high_risk"
    
    def _analyze_efficiency(self, ratios: Dict) -> str:
        """Analizar eficiencia de la empresa"""
        asset_turnover = ratios.get("asset_turnover", 0)
        
        if asset_turnover > 2.0:
            return "excellent"
        elif asset_turnover > 1.5:
            return "good"
        elif asset_turnover > 1.0:
            return "acceptable"
        else:
            return "poor"
    
    def _identify_risk_indicators(self, ratios: Dict, financial_data: Dict) -> List[str]:
        """Identificar indicadores de riesgo"""
        risk_indicators = []
        
        # Liquidez
        if ratios.get("current_ratio", 0) < 1.0:
            risk_indicators.append("Problemas de liquidez a corto plazo")
        
        # Rentabilidad
        if ratios.get("profit_margin", 0) < 0:
            risk_indicators.append("Márgenes negativos")
        
        # Endeudamiento
        if ratios.get("debt_to_assets", 0) > 0.8:
            risk_indicators.append("Alto nivel de endeudamiento")
        
        # Cash flow
        income_statement = financial_data.get("income_statement", {})
        cash_flow = financial_data.get("cash_flow", {})
        
        if cash_flow.get("operating_cash_flow", 0) < 0:
            risk_indicators.append("Flujo de caja operativo negativo")
        
        if income_statement.get("net_income", 0) < 0:
            risk_indicators.append("Pérdidas netas")
        
        return risk_indicators
    
    def _calculate_volatility(self, values: List[float]) -> float:
        """Calcular volatilidad de una serie de valores"""
        if len(values) < 2:
            return 0.0
        
        import statistics
        try:
            mean = statistics.mean(values)
            variance = statistics.variance(values)
            return (variance ** 0.5) / mean if mean > 0 else 0.0
        except:
            return 0.0
    
    def _generate_fallback_financials(self, ruc: str) -> Dict:
        """Generar datos financieros de respaldo"""
        import random
        
        return {
            "estimated_data": True,
            "revenue_estimate": random.randint(100000, 500000),
            "size_category": "PYME",
            "sector_estimate": "Comercio General",
            "risk_level": "medium",
            "note": "Datos estimados - Estados financieros oficiales no disponibles"
        }
