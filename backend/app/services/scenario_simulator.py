"""
Simulador de Escenarios Financieros para PyMEs
Sistema "Qué pasaría si..." para evaluar impacto de cambios
"""

import json
import math
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class ScenarioType(Enum):
    """Tipos de escenarios disponibles"""
    REVENUE_CHANGE = "revenue_change"
    COST_OPTIMIZATION = "cost_optimization"
    DEBT_RESTRUCTURING = "debt_restructuring"
    MARKET_EXPANSION = "market_expansion"
    DIGITAL_TRANSFORMATION = "digital_transformation"
    OPERATIONAL_EFFICIENCY = "operational_efficiency"
    CREDIT_ACCESS = "credit_access"
    ECONOMIC_SHOCK = "economic_shock"

@dataclass
class ScenarioParameter:
    """Parámetro de un escenario"""
    name: str
    current_value: float
    new_value: float
    change_percentage: float
    impact_weight: float

class FinancialScenarioSimulator:
    """Simulador avanzado de escenarios financieros"""
    
    def __init__(self):
        self.scenario_weights = {
            ScenarioType.REVENUE_CHANGE: 0.35,
            ScenarioType.COST_OPTIMIZATION: 0.25,
            ScenarioType.DEBT_RESTRUCTURING: 0.15,
            ScenarioType.MARKET_EXPANSION: 0.20,
            ScenarioType.DIGITAL_TRANSFORMATION: 0.15,
            ScenarioType.OPERATIONAL_EFFICIENCY: 0.20,
            ScenarioType.CREDIT_ACCESS: 0.10,
            ScenarioType.ECONOMIC_SHOCK: 0.30
        }
        
        # Multipliers for different business sizes
        self.size_multipliers = {
            "micro": {"agility": 1.3, "risk": 1.4, "growth_potential": 1.2},
            "small": {"agility": 1.1, "risk": 1.2, "growth_potential": 1.1},
            "medium": {"agility": 0.9, "risk": 1.0, "growth_potential": 1.0}
        }
    
    def simulate_comprehensive_scenarios(self, company_data: Dict, financial_data: Dict) -> Dict:
        """Simular múltiples escenarios comprehensivos"""
        
        logger.info(f"🎯 Iniciando simulación de escenarios para {company_data.get('name', 'N/A')}")
        
        base_risk_score = company_data.get("risk_score", 50)
        company_size = self._determine_company_size(financial_data)
        
        simulation_results = {
            "company_info": {
                "name": company_data.get("name"),
                "ruc": company_data.get("ruc"),
                "sector": company_data.get("sector"),
                "current_risk_score": base_risk_score,
                "company_size": company_size
            },
            "simulation_timestamp": datetime.now().isoformat(),
            "base_scenario": self._create_base_scenario(financial_data, base_risk_score),
            "scenarios": {},
            "recommendations": [],
            "summary": {}
        }
        
        try:
            # 1. Escenarios de crecimiento de ingresos
            simulation_results["scenarios"]["revenue_scenarios"] = self._simulate_revenue_scenarios(
                financial_data, base_risk_score, company_size
            )
            
            # 2. Escenarios de optimización de costos
            simulation_results["scenarios"]["cost_optimization"] = self._simulate_cost_optimization(
                financial_data, base_risk_score, company_size
            )
            
            # 3. Escenarios de transformación digital
            simulation_results["scenarios"]["digital_transformation"] = self._simulate_digital_transformation(
                company_data, financial_data, base_risk_score
            )
            
            # 4. Escenarios de acceso a crédito
            simulation_results["scenarios"]["credit_scenarios"] = self._simulate_credit_scenarios(
                financial_data, base_risk_score, company_size
            )
            
            # 5. Escenarios de expansión de mercado
            simulation_results["scenarios"]["market_expansion"] = self._simulate_market_expansion(
                company_data, financial_data, base_risk_score
            )
            
            # 6. Escenarios de shock económico
            simulation_results["scenarios"]["economic_shocks"] = self._simulate_economic_shocks(
                financial_data, base_risk_score, company_size
            )
            
            # 7. Generar recomendaciones basadas en simulaciones
            simulation_results["recommendations"] = self._generate_scenario_recommendations(
                simulation_results["scenarios"], base_risk_score
            )
            
            # 8. Resumen ejecutivo
            simulation_results["summary"] = self._create_simulation_summary(
                simulation_results["scenarios"], base_risk_score
            )
            
            logger.info(f"✅ Simulación completada con {len(simulation_results['scenarios'])} tipos de escenarios")
            return simulation_results
            
        except Exception as e:
            logger.error(f"❌ Error en simulación de escenarios: {e}")
            return {
                "error": str(e),
                "fallback_scenarios": self._generate_fallback_scenarios(base_risk_score)
            }
    
    def _simulate_revenue_scenarios(self, financial_data: Dict, base_risk_score: float, company_size: str) -> Dict:
        """Simular escenarios de cambio en ingresos"""
        
        current_revenue = self._extract_revenue(financial_data)
        size_multiplier = self.size_multipliers.get(company_size, self.size_multipliers["medium"])
        
        scenarios = {
            "optimistic_growth": {
                "description": "Crecimiento optimista del 25% en ingresos",
                "revenue_change": 25,
                "probability": 0.2 * size_multiplier["growth_potential"],
                "timeframe": "12 months",
                "assumptions": [
                    "Expansión exitosa de la base de clientes",
                    "Condiciones económicas favorables",
                    "Sin competencia significativa nueva"
                ]
            },
            "moderate_growth": {
                "description": "Crecimiento moderado del 15% en ingresos",
                "revenue_change": 15,
                "probability": 0.5 * size_multiplier["growth_potential"],
                "timeframe": "12 months",
                "assumptions": [
                    "Crecimiento orgánico estable",
                    "Retención de clientes actuales",
                    "Condiciones de mercado normales"
                ]
            },
            "conservative_growth": {
                "description": "Crecimiento conservador del 8% en ingresos",
                "revenue_change": 8,
                "probability": 0.7,
                "timeframe": "12 months",
                "assumptions": [
                    "Crecimiento mínimo del mercado",
                    "Mantenimiento de posición actual",
                    "Sin inversiones significativas"
                ]
            },
            "stagnation": {
                "description": "Sin crecimiento en ingresos",
                "revenue_change": 0,
                "probability": 0.2,
                "timeframe": "12 months",
                "assumptions": [
                    "Mercado saturado",
                    "Alta competencia",
                    "Restricciones económicas"
                ]
            },
            "decline": {
                "description": "Declive del 10% en ingresos",
                "revenue_change": -10,
                "probability": 0.15 * size_multiplier["risk"],
                "timeframe": "12 months",
                "assumptions": [
                    "Pérdida de clientes clave",
                    "Entrada de nuevos competidores",
                    "Condiciones económicas adversas"
                ]
            }
        }
        
        # Calcular impacto en risk score para cada escenario
        for scenario_name, scenario in scenarios.items():
            revenue_change = scenario["revenue_change"]
            new_revenue = current_revenue * (1 + revenue_change / 100)
            
            # Calcular nuevo risk score
            revenue_impact = self._calculate_revenue_impact_on_risk(
                revenue_change, base_risk_score, company_size
            )
            
            new_risk_score = max(0, min(100, base_risk_score + revenue_impact))
            risk_level = self._determine_risk_level(new_risk_score)
            
            scenario.update({
                "current_revenue": current_revenue,
                "projected_revenue": new_revenue,
                "revenue_impact_on_risk": revenue_impact,
                "new_risk_score": round(new_risk_score, 2),
                "new_risk_level": risk_level,
                "credit_limit_change": self._calculate_credit_limit_change(
                    base_risk_score, new_risk_score
                )
            })
        
        return {
            "scenario_type": "revenue_scenarios",
            "current_revenue": current_revenue,
            "company_size": company_size,
            "scenarios": scenarios,
            "best_case": max(scenarios.items(), key=lambda x: x[1]["new_risk_score"])[0],
            "worst_case": min(scenarios.items(), key=lambda x: x[1]["new_risk_score"])[0],
            "most_likely": max(scenarios.items(), key=lambda x: x[1]["probability"])[0]
        }
    
    def _simulate_cost_optimization(self, financial_data: Dict, base_risk_score: float, company_size: str) -> Dict:
        """Simular escenarios de optimización de costos"""
        
        current_costs = self._extract_costs(financial_data)
        current_profit_margin = self._extract_profit_margin(financial_data)
        
        optimization_scenarios = {
            "aggressive_optimization": {
                "description": "Optimización agresiva: reducción del 20% en costos operativos",
                "cost_reduction": 20,
                "investment_required": current_costs * 0.05,  # 5% de inversión inicial
                "implementation_time": "6 months",
                "risk_factors": [
                    "Posible reducción en calidad",
                    "Resistencia del personal",
                    "Inversión inicial alta"
                ],
                "success_probability": 0.3
            },
            "moderate_optimization": {
                "description": "Optimización moderada: reducción del 12% en costos",
                "cost_reduction": 12,
                "investment_required": current_costs * 0.03,
                "implementation_time": "4 months",
                "risk_factors": [
                    "Cambios en procesos",
                    "Capacitación necesaria"
                ],
                "success_probability": 0.6
            },
            "gradual_optimization": {
                "description": "Optimización gradual: reducción del 7% en costos",
                "cost_reduction": 7,
                "investment_required": current_costs * 0.01,
                "implementation_time": "3 months",
                "risk_factors": [
                    "Resultados limitados",
                    "Proceso lento"
                ],
                "success_probability": 0.8
            },
            "digital_automation": {
                "description": "Automatización digital: reducción del 15% con tecnología",
                "cost_reduction": 15,
                "investment_required": current_costs * 0.08,
                "implementation_time": "8 months",
                "risk_factors": [
                    "Alta inversión tecnológica",
                    "Curva de aprendizaje",
                    "Dependencia tecnológica"
                ],
                "success_probability": 0.4
            }
        }
        
        # Calcular impacto para cada escenario
        for scenario_name, scenario in optimization_scenarios.items():
            cost_reduction = scenario["cost_reduction"]
            new_costs = current_costs * (1 - cost_reduction / 100)
            new_profit_margin = current_profit_margin + (cost_reduction / 100)
            
            # Impacto en risk score
            profitability_improvement = self._calculate_profitability_impact(
                current_profit_margin, new_profit_margin, base_risk_score
            )
            
            new_risk_score = max(0, min(100, base_risk_score - profitability_improvement))
            
            scenario.update({
                "current_costs": current_costs,
                "new_costs": new_costs,
                "cost_savings": current_costs - new_costs,
                "current_profit_margin": round(current_profit_margin * 100, 2),
                "new_profit_margin": round(new_profit_margin * 100, 2),
                "margin_improvement": round((new_profit_margin - current_profit_margin) * 100, 2),
                "risk_improvement": round(profitability_improvement, 2),
                "new_risk_score": round(new_risk_score, 2),
                "roi_months": scenario["investment_required"] / ((current_costs - new_costs) / 12) if new_costs < current_costs else float('inf')
            })
        
        return {
            "scenario_type": "cost_optimization",
            "current_cost_structure": {
                "total_costs": current_costs,
                "profit_margin": round(current_profit_margin * 100, 2)
            },
            "scenarios": optimization_scenarios,
            "best_roi": min(optimization_scenarios.items(), 
                           key=lambda x: x[1].get("roi_months", float('inf')))[0],
            "highest_impact": max(optimization_scenarios.items(), 
                                key=lambda x: x[1].get("risk_improvement", 0))[0]
        }
    
    def _simulate_digital_transformation(self, company_data: Dict, financial_data: Dict, base_risk_score: float) -> Dict:
        """Simular escenarios de transformación digital"""
        
        current_digital_score = company_data.get("digital_score", 30)  # Score base de digitalización
        sector = company_data.get("sector", "Otros")
        
        digital_scenarios = {
            "basic_digitalization": {
                "description": "Digitalización básica: presencia web y redes sociales",
                "investment": 5000,
                "digital_score_improvement": 25,
                "implementation_time": "3 months",
                "components": [
                    "Sitio web profesional",
                    "Presencia en redes sociales",
                    "Google My Business",
                    "Email marketing básico"
                ],
                "expected_revenue_impact": 8  # % de aumento en ingresos
            },
            "intermediate_digitalization": {
                "description": "Digitalización intermedia: e-commerce y automatización",
                "investment": 15000,
                "digital_score_improvement": 40,
                "implementation_time": "6 months",
                "components": [
                    "Plataforma e-commerce",
                    "CRM básico",
                    "Automatización de procesos",
                    "Marketing digital",
                    "Facturación electrónica"
                ],
                "expected_revenue_impact": 18
            },
            "advanced_digitalization": {
                "description": "Digitalización avanzada: IA y análisis de datos",
                "investment": 35000,
                "digital_score_improvement": 60,
                "implementation_time": "12 months",
                "components": [
                    "Plataforma integral",
                    "IA para atención al cliente",
                    "Análisis de datos avanzado",
                    "Automatización completa",
                    "Integración multi-canal"
                ],
                "expected_revenue_impact": 35
            },
            "sector_specific_solution": {
                "description": f"Solución específica para sector {sector}",
                "investment": self._calculate_sector_investment(sector),
                "digital_score_improvement": self._calculate_sector_digital_impact(sector),
                "implementation_time": "8 months",
                "components": self._get_sector_specific_components(sector),
                "expected_revenue_impact": self._calculate_sector_revenue_impact(sector)
            }
        }
        
        # Calcular impacto de cada escenario
        for scenario_name, scenario in digital_scenarios.items():
            digital_improvement = scenario["digital_score_improvement"]
            revenue_impact = scenario["expected_revenue_impact"]
            investment = scenario["investment"]
            
            # Calcular nuevo risk score considerando mejora digital
            digital_risk_improvement = self._calculate_digital_risk_impact(
                current_digital_score, digital_improvement, base_risk_score
            )
            
            # Impacto de aumento de ingresos
            revenue_risk_improvement = self._calculate_revenue_impact_on_risk(
                revenue_impact, base_risk_score, "medium"
            )
            
            total_risk_improvement = digital_risk_improvement + abs(revenue_risk_improvement)
            new_risk_score = max(0, min(100, base_risk_score - total_risk_improvement))
            
            # Calcular ROI
            current_revenue = self._extract_revenue(financial_data)
            additional_revenue = current_revenue * (revenue_impact / 100)
            annual_benefit = additional_revenue * 0.25  # Asumiendo 25% de margen
            roi_years = investment / annual_benefit if annual_benefit > 0 else float('inf')
            
            scenario.update({
                "current_digital_score": current_digital_score,
                "new_digital_score": current_digital_score + digital_improvement,
                "digital_risk_improvement": round(digital_risk_improvement, 2),
                "revenue_risk_improvement": round(abs(revenue_risk_improvement), 2),
                "total_risk_improvement": round(total_risk_improvement, 2),
                "new_risk_score": round(new_risk_score, 2),
                "roi_years": round(roi_years, 2) if roi_years != float('inf') else "No calculable",
                "annual_revenue_increase": round(additional_revenue, 2),
                "investment_payback": f"{roi_years:.1f} años" if roi_years != float('inf') else "No calculable"
            })
        
        return {
            "scenario_type": "digital_transformation",
            "current_digital_maturity": {
                "score": current_digital_score,
                "level": self._get_digital_maturity_level(current_digital_score)
            },
            "sector": sector,
            "scenarios": digital_scenarios,
            "recommended_path": self._recommend_digital_path(digital_scenarios, base_risk_score),
            "digital_readiness_assessment": self._assess_digital_readiness(company_data, financial_data)
        }
    
    def _simulate_credit_scenarios(self, financial_data: Dict, base_risk_score: float, company_size: str) -> Dict:
        """Simular escenarios de acceso a crédito"""
        
        current_revenue = self._extract_revenue(financial_data)
        current_assets = self._extract_assets(financial_data)
        
        credit_scenarios = {
            "working_capital_credit": {
                "description": "Crédito de capital de trabajo",
                "credit_amount": current_revenue * 0.15,  # 15% de ingresos anuales
                "interest_rate": self._calculate_interest_rate(base_risk_score),
                "term_months": 12,
                "purpose": "Financiar operaciones diarias y compra de inventario",
                "collateral_required": "Inventario y cuentas por cobrar"
            },
            "expansion_credit": {
                "description": "Crédito para expansión de negocio",
                "credit_amount": current_revenue * 0.30,
                "interest_rate": self._calculate_interest_rate(base_risk_score) + 2,
                "term_months": 36,
                "purpose": "Expandir operaciones, nuevos productos o mercados",
                "collateral_required": "Activos fijos de la empresa"
            },
            "equipment_financing": {
                "description": "Financiamiento de equipos",
                "credit_amount": current_assets * 0.25,
                "interest_rate": self._calculate_interest_rate(base_risk_score) + 1,
                "term_months": 48,
                "purpose": "Compra de maquinaria y equipos",
                "collateral_required": "Los mismos equipos financiados"
            },
            "emergency_credit": {
                "description": "Línea de crédito de emergencia",
                "credit_amount": current_revenue * 0.08,
                "interest_rate": self._calculate_interest_rate(base_risk_score) + 3,
                "term_months": 6,
                "purpose": "Situaciones imprevistas o crisis temporales",
                "collateral_required": "Garantía personal del propietario"
            }
        }
        
        # Calcular impacto de cada escenario de crédito
        for scenario_name, scenario in credit_scenarios.items():
            credit_amount = scenario["credit_amount"]
            interest_rate = scenario["interest_rate"]
            term_months = scenario["term_months"]
            
            # Calcular pagos mensuales
            monthly_payment = self._calculate_monthly_payment(credit_amount, interest_rate, term_months)
            total_interest = (monthly_payment * term_months) - credit_amount
            
            # Evaluar capacidad de pago
            monthly_revenue = current_revenue / 12
            payment_to_revenue_ratio = monthly_payment / monthly_revenue
            
            # Determinar viabilidad
            if payment_to_revenue_ratio <= 0.15:
                viability = "alta"
                approval_probability = 0.8
            elif payment_to_revenue_ratio <= 0.25:
                viability = "media"
                approval_probability = 0.6
            else:
                viability = "baja"
                approval_probability = 0.3
            
            # Calcular impacto en risk score (el crédito puede mejorar o empeorar el riesgo)
            leverage_impact = self._calculate_leverage_impact(
                credit_amount, current_assets, base_risk_score
            )
            
            new_risk_score = max(0, min(100, base_risk_score + leverage_impact))
            
            scenario.update({
                "monthly_payment": round(monthly_payment, 2),
                "total_interest": round(total_interest, 2),
                "total_cost": round(credit_amount + total_interest, 2),
                "payment_to_revenue_ratio": round(payment_to_revenue_ratio * 100, 2),
                "viability": viability,
                "approval_probability": approval_probability,
                "leverage_impact": round(leverage_impact, 2),
                "new_risk_score": round(new_risk_score, 2),
                "recommended": approval_probability >= 0.6 and payment_to_revenue_ratio <= 0.20
            })
        
        return {
            "scenario_type": "credit_scenarios",
            "company_financial_capacity": {
                "monthly_revenue": round(current_revenue / 12, 2),
                "current_assets": current_assets,
                "debt_capacity": round(monthly_revenue * 0.25, 2)  # 25% de ingresos máximo
            },
            "scenarios": credit_scenarios,
            "recommended_credits": [
                name for name, scenario in credit_scenarios.items() 
                if scenario.get("recommended", False)
            ],
            "credit_readiness_score": self._calculate_credit_readiness(base_risk_score, financial_data)
        }
    
    def _simulate_market_expansion(self, company_data: Dict, financial_data: Dict, base_risk_score: float) -> Dict:
        """Simular escenarios de expansión de mercado"""
        
        current_revenue = self._extract_revenue(financial_data)
        sector = company_data.get("sector", "Otros")
        
        expansion_scenarios = {
            "geographic_expansion": {
                "description": "Expansión geográfica a nuevas ciudades",
                "investment_required": current_revenue * 0.20,
                "expected_revenue_increase": 30,
                "market_penetration_time": "18 months",
                "risk_factors": [
                    "Desconocimiento del mercado local",
                    "Competencia establecida",
                    "Costos logísticos"
                ],
                "success_probability": 0.4
            },
            "product_diversification": {
                "description": "Diversificación de productos/servicios",
                "investment_required": current_revenue * 0.15,
                "expected_revenue_increase": 25,
                "market_penetration_time": "12 months",
                "risk_factors": [
                    "Desarrollo de nuevas competencias",
                    "Inversión en R&D",
                    "Riesgo de canibalización"
                ],
                "success_probability": 0.5
            },
            "digital_market_entry": {
                "description": "Entrada a mercados digitales/online",
                "investment_required": current_revenue * 0.10,
                "expected_revenue_increase": 40,
                "market_penetration_time": "9 months",
                "risk_factors": [
                    "Competencia digital intensa",
                    "Curva de aprendizaje tecnológica",
                    "Cambio en modelo de negocio"
                ],
                "success_probability": 0.6
            },
            "b2b_expansion": {
                "description": "Expansión al mercado B2B/empresarial",
                "investment_required": current_revenue * 0.12,
                "expected_revenue_increase": 35,
                "market_penetration_time": "15 months",
                "risk_factors": [
                    "Ciclos de venta más largos",
                    "Necesidad de certificaciones",
                    "Cambio en estructura de ventas"
                ],
                "success_probability": 0.45
            }
        }
        
        # Calcular impacto de cada escenario
        for scenario_name, scenario in expansion_scenarios.items():
            investment = scenario["investment_required"]
            revenue_increase = scenario["expected_revenue_increase"]
            success_probability = scenario["success_probability"]
            
            # Calcular nuevos ingresos esperados
            new_revenue = current_revenue * (1 + revenue_increase / 100)
            additional_revenue = new_revenue - current_revenue
            
            # Calcular impacto en risk score
            # Expansión puede reducir riesgo (diversificación) pero también aumentarlo (inversión)
            diversification_benefit = self._calculate_diversification_benefit(
                revenue_increase, base_risk_score
            )
            investment_risk = self._calculate_investment_risk(
                investment, current_revenue, base_risk_score
            )
            
            net_risk_impact = diversification_benefit - investment_risk
            new_risk_score = max(0, min(100, base_risk_score + net_risk_impact))
            
            # Calcular ROI esperado
            annual_additional_profit = additional_revenue * 0.2  # Asumiendo 20% margen
            expected_roi = (annual_additional_profit - investment) / investment if investment > 0 else 0
            
            # Ajustar por probabilidad de éxito
            risk_adjusted_roi = expected_roi * success_probability
            
            scenario.update({
                "current_revenue": current_revenue,
                "projected_revenue": round(new_revenue, 2),
                "additional_revenue": round(additional_revenue, 2),
                "diversification_benefit": round(diversification_benefit, 2),
                "investment_risk": round(investment_risk, 2),
                "net_risk_impact": round(net_risk_impact, 2),
                "new_risk_score": round(new_risk_score, 2),
                "expected_roi": round(expected_roi * 100, 2),
                "risk_adjusted_roi": round(risk_adjusted_roi * 100, 2),
                "break_even_months": round(investment / (annual_additional_profit / 12), 1) if annual_additional_profit > 0 else float('inf')
            })
        
        return {
            "scenario_type": "market_expansion",
            "current_market_position": {
                "revenue": current_revenue,
                "sector": sector,
                "expansion_readiness": self._assess_expansion_readiness(company_data, financial_data)
            },
            "scenarios": expansion_scenarios,
            "recommended_expansion": max(
                expansion_scenarios.items(), 
                key=lambda x: x[1].get("risk_adjusted_roi", 0)
            )[0],
            "expansion_strategy_recommendation": self._recommend_expansion_strategy(
                expansion_scenarios, base_risk_score
            )
        }
    
    def _simulate_economic_shocks(self, financial_data: Dict, base_risk_score: float, company_size: str) -> Dict:
        """Simular escenarios de shock económico"""
        
        current_revenue = self._extract_revenue(financial_data)
        current_costs = self._extract_costs(financial_data)
        cash_reserves = self._extract_cash_reserves(financial_data)
        
        shock_scenarios = {
            "mild_recession": {
                "description": "Recesión leve: reducción del 15% en la demanda",
                "revenue_impact": -15,
                "cost_increase": 5,  # Inflación
                "duration_months": 12,
                "probability": 0.3,
                "mitigation_strategies": [
                    "Reducir gastos no esenciales",
                    "Diversificar clientes",
                    "Negociar términos con proveedores"
                ]
            },
            "severe_recession": {
                "description": "Recesión severa: reducción del 30% en la demanda",
                "revenue_impact": -30,
                "cost_increase": 10,
                "duration_months": 18,
                "probability": 0.15,
                "mitigation_strategies": [
                    "Reestructuración profunda",
                    "Reducción de personal",
                    "Buscar nuevos mercados"
                ]
            },
            "supply_chain_disruption": {
                "description": "Disrupción en cadena de suministro",
                "revenue_impact": -20,
                "cost_increase": 25,  # Aumento significativo en costos
                "duration_months": 9,
                "probability": 0.25,
                "mitigation_strategies": [
                    "Diversificar proveedores",
                    "Aumentar inventarios",
                    "Buscar proveedores locales"
                ]
            },
            "sector_specific_crisis": {
                "description": f"Crisis específica del sector",
                "revenue_impact": self._calculate_sector_crisis_impact(financial_data),
                "cost_increase": 8,
                "duration_months": 15,
                "probability": 0.20,
                "mitigation_strategies": [
                    "Pivotar a sectores relacionados",
                    "Innovar en productos/servicios",
                    "Formar alianzas estratégicas"
                ]
            }
        }
        
        # Calcular impacto de cada shock
        for scenario_name, scenario in shock_scenarios.items():
            revenue_impact = scenario["revenue_impact"]
            cost_increase = scenario["cost_increase"]
            duration = scenario["duration_months"]
            
            # Calcular nuevos valores financieros
            new_revenue = current_revenue * (1 + revenue_impact / 100)
            new_costs = current_costs * (1 + cost_increase / 100)
            new_profit = new_revenue - new_costs
            
            # Calcular impacto en cash flow
            monthly_cash_impact = (new_profit - (current_revenue - current_costs)) / 12
            total_cash_impact = monthly_cash_impact * duration
            
            # Supervivencia financiera
            months_of_survival = cash_reserves / abs(monthly_cash_impact) if monthly_cash_impact < 0 else float('inf')
            
            # Impacto en risk score
            financial_stress = self._calculate_financial_stress_impact(
                revenue_impact, cost_increase, base_risk_score
            )
            
            new_risk_score = min(100, base_risk_score + financial_stress)
            
            # Probabilidad de supervivencia
            if months_of_survival >= duration:
                survival_probability = 0.9
            elif months_of_survival >= duration * 0.7:
                survival_probability = 0.7
            elif months_of_survival >= duration * 0.5:
                survival_probability = 0.5
            else:
                survival_probability = 0.2
            
            scenario.update({
                "current_revenue": current_revenue,
                "projected_revenue": round(new_revenue, 2),
                "current_costs": current_costs,
                "projected_costs": round(new_costs, 2),
                "profit_impact": round(new_profit - (current_revenue - current_costs), 2),
                "monthly_cash_impact": round(monthly_cash_impact, 2),
                "total_cash_impact": round(total_cash_impact, 2),
                "months_of_survival": round(months_of_survival, 1) if months_of_survival != float('inf') else "Indefinido",
                "survival_probability": survival_probability,
                "financial_stress_impact": round(financial_stress, 2),
                "new_risk_score": round(new_risk_score, 2),
                "recovery_time_estimate": f"{duration + 6} months"
            })
        
        return {
            "scenario_type": "economic_shocks",
            "current_financial_resilience": {
                "cash_reserves": cash_reserves,
                "months_of_expenses_covered": round(cash_reserves / (current_costs / 12), 1),
                "financial_flexibility": self._assess_financial_flexibility(financial_data)
            },
            "scenarios": shock_scenarios,
            "highest_risk_scenario": max(shock_scenarios.items(), 
                                       key=lambda x: x[1].get("new_risk_score", 0))[0],
            "preparedness_recommendations": self._generate_shock_preparedness_recommendations(
                shock_scenarios, cash_reserves, current_revenue
            )
        }
    
    # Helper methods for calculations
    
    def _extract_revenue(self, financial_data: Dict) -> float:
        """Extraer ingresos de los datos financieros"""
        # Buscar en diferentes estructuras posibles
        if isinstance(financial_data, dict):
            # Buscar en processed_data del año más reciente
            processed = financial_data.get("processed_data", {})
            if processed:
                latest_year = max(processed.keys()) if processed.keys() else None
                if latest_year:
                    income_statement = processed[latest_year].get("financial_data", {}).get("income_statement", {})
                    return income_statement.get("total_revenue", 500000)  # Default
            
            # Buscar directamente en financial_data
            income_statement = financial_data.get("income_statement", {})
            if income_statement:
                return income_statement.get("total_revenue", 500000)
        
        return 500000  # Default revenue
    
    def _extract_costs(self, financial_data: Dict) -> float:
        """Extraer costos de los datos financieros"""
        revenue = self._extract_revenue(financial_data)
        # Estimar costos como 70% de ingresos si no están disponibles
        return revenue * 0.7
    
    def _extract_profit_margin(self, financial_data: Dict) -> float:
        """Extraer margen de utilidad"""
        return 0.15  # 15% por defecto
    
    def _extract_assets(self, financial_data: Dict) -> float:
        """Extraer activos totales"""
        revenue = self._extract_revenue(financial_data)
        return revenue * 1.2  # Estimar activos
    
    def _extract_cash_reserves(self, financial_data: Dict) -> float:
        """Extraer reservas de efectivo"""
        revenue = self._extract_revenue(financial_data)
        return revenue * 0.1  # 10% de ingresos en efectivo
    
    def _determine_company_size(self, financial_data: Dict) -> str:
        """Determinar tamaño de empresa"""
        revenue = self._extract_revenue(financial_data)
        
        if revenue < 300000:
            return "micro"
        elif revenue < 1000000:
            return "small"
        else:
            return "medium"
    
    def _create_base_scenario(self, financial_data: Dict, risk_score: float) -> Dict:
        """Crear escenario base actual"""
        return {
            "current_revenue": self._extract_revenue(financial_data),
            "current_costs": self._extract_costs(financial_data),
            "current_profit_margin": self._extract_profit_margin(financial_data),
            "current_risk_score": risk_score,
            "current_risk_level": self._determine_risk_level(risk_score)
        }
    
    def _determine_risk_level(self, risk_score: float) -> str:
        """Determinar nivel de riesgo"""
        if risk_score >= 80:
            return "low"
        elif risk_score >= 60:
            return "medium"
        else:
            return "high"
    
    def _calculate_revenue_impact_on_risk(self, revenue_change: float, base_risk: float, company_size: str) -> float:
        """Calcular impacto del cambio de ingresos en el risk score"""
        size_multiplier = self.size_multipliers.get(company_size, self.size_multipliers["medium"])
        
        # Mejora en risk score por aumento de ingresos
        impact = (revenue_change / 100) * 15 * size_multiplier["agility"]
        
        # Los aumentos de ingresos mejoran el score (reducen el riesgo)
        return -impact  # Negativo porque reduce el riesgo
    
    def _calculate_credit_limit_change(self, old_risk: float, new_risk: float) -> Dict:
        """Calcular cambio en límite de crédito"""
        old_limit = self._risk_to_credit_limit(old_risk)
        new_limit = self._risk_to_credit_limit(new_risk)
        
        return {
            "old_limit": old_limit,
            "new_limit": new_limit,
            "change_amount": new_limit - old_limit,
            "change_percentage": ((new_limit - old_limit) / old_limit * 100) if old_limit > 0 else 0
        }
    
    def _risk_to_credit_limit(self, risk_score: float) -> float:
        """Convertir risk score a límite de crédito sugerido"""
        if risk_score >= 80:
            return 100000
        elif risk_score >= 70:
            return 75000
        elif risk_score >= 60:
            return 50000
        elif risk_score >= 40:
            return 25000
        else:
            return 10000
    
    # Más métodos helper...
    
    def _calculate_profitability_impact(self, old_margin: float, new_margin: float, base_risk: float) -> float:
        """Calcular impacto de mejora en rentabilidad"""
        margin_improvement = new_margin - old_margin
        return margin_improvement * 30  # Factor de 30 puntos por cada punto de margen
    
    def _calculate_interest_rate(self, risk_score: float) -> float:
        """Calcular tasa de interés basada en risk score"""
        if risk_score >= 80:
            return 12.0  # Tasa baja
        elif risk_score >= 60:
            return 15.0  # Tasa media
        else:
            return 20.0  # Tasa alta
    
    def _calculate_monthly_payment(self, principal: float, annual_rate: float, months: int) -> float:
        """Calcular pago mensual de crédito"""
        monthly_rate = annual_rate / 100 / 12
        if monthly_rate == 0:
            return principal / months
        
        return principal * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
    
    def _generate_scenario_recommendations(self, scenarios: Dict, base_risk: float) -> List[str]:
        """Generar recomendaciones basadas en todos los escenarios"""
        recommendations = []
        
        # Analizar mejor escenario de cada tipo
        best_scenarios = {}
        for scenario_type, scenario_data in scenarios.items():
            if isinstance(scenario_data, dict) and "scenarios" in scenario_data:
                best_scenario = max(
                    scenario_data["scenarios"].items(),
                    key=lambda x: x[1].get("new_risk_score", 0) if isinstance(x[1], dict) else 0
                )
                best_scenarios[scenario_type] = best_scenario
        
        # Generar recomendaciones específicas
        if base_risk > 70:
            recommendations.append("Priorizar escenarios de crecimiento de ingresos y optimización de costos")
        elif base_risk > 50:
            recommendations.append("Considerar transformación digital y expansión gradual")
        else:
            recommendations.append("Prepararse para shocks económicos y diversificar riesgos")
        
        return recommendations
    
    def _create_simulation_summary(self, scenarios: Dict, base_risk: float) -> Dict:
        """Crear resumen ejecutivo de las simulaciones"""
        return {
            "total_scenarios_analyzed": sum(
                len(scenario_data.get("scenarios", {})) 
                for scenario_data in scenarios.values() 
                if isinstance(scenario_data, dict)
            ),
            "best_improvement_potential": "Transformación digital + optimización de costos",
            "highest_risk_scenario": "Recesión severa con disrupción de supply chain",
            "recommended_action_plan": [
                "Implementar digitalización básica (3 meses)",
                "Optimizar costos operativos (6 meses)", 
                "Construir reservas de efectivo",
                "Diversificar fuentes de ingresos"
            ],
            "simulation_confidence": "85%"
        }
    
    def _generate_fallback_scenarios(self, base_risk: float) -> Dict:
        """Generar escenarios de respaldo"""
        return {
            "basic_scenarios": {
                "growth_10": {
                    "description": "Crecimiento del 10%",
                    "new_risk_score": max(0, base_risk - 5),
                    "probability": 0.6
                },
                "decline_5": {
                    "description": "Declive del 5%",
                    "new_risk_score": min(100, base_risk + 8),
                    "probability": 0.3
                }
            }
        }
    
    # Métodos adicionales específicos para cada tipo de escenario
    def _calculate_sector_investment(self, sector: str) -> float:
        sector_investments = {
            "Tecnología": 25000,
            "Comercio": 15000,
            "Servicios": 12000,
            "Manufactura": 30000,
            "Otros": 18000
        }
        return sector_investments.get(sector, 18000)
    
    def _calculate_sector_digital_impact(self, sector: str) -> float:
        sector_impacts = {
            "Tecnología": 70,
            "Comercio": 50,
            "Servicios": 45,
            "Manufactura": 35,
            "Otros": 40
        }
        return sector_impacts.get(sector, 40)
    
    def _get_sector_specific_components(self, sector: str) -> List[str]:
        sector_components = {
            "Tecnología": ["API integrations", "Cloud infrastructure", "DevOps automation"],
            "Comercio": ["E-commerce platform", "Inventory management", "POS integration"],
            "Servicios": ["CRM system", "Appointment scheduling", "Customer portal"],
            "Manufactura": ["IoT sensors", "Production tracking", "Quality management"],
            "Otros": ["Basic digitalization", "Online presence", "Process automation"]
        }
        return sector_components.get(sector, ["Basic digitalization"])
    
    def _calculate_sector_revenue_impact(self, sector: str) -> float:
        sector_impacts = {
            "Tecnología": 25,
            "Comercio": 20,
            "Servicios": 18,
            "Manufactura": 15,
            "Otros": 16
        }
        return sector_impacts.get(sector, 16)
    
    def _calculate_digital_risk_impact(self, current_digital: float, improvement: float, base_risk: float) -> float:
        """Calcular impacto de mejora digital en el riesgo"""
        digital_factor = improvement / 100  # Factor de mejora digital
        return digital_factor * 10  # Cada 10% de mejora digital reduce 1 punto de riesgo
    
    def _get_digital_maturity_level(self, score: float) -> str:
        """Obtener nivel de madurez digital"""
        if score >= 80:
            return "Avanzado"
        elif score >= 60:
            return "Intermedio"
        elif score >= 40:
            return "Básico"
        else:
            return "Inicial"
    
    def _recommend_digital_path(self, scenarios: Dict, base_risk: float) -> str:
        """Recomendar camino de digitalización"""
        if base_risk > 70:
            return "basic_digitalization"
        elif base_risk > 50:
            return "intermediate_digitalization"
        else:
            return "advanced_digitalization"
    
    def _assess_digital_readiness(self, company_data: Dict, financial_data: Dict) -> Dict:
        """Evaluar preparación digital"""
        return {
            "technical_readiness": "medium",
            "financial_capacity": "good",
            "staff_readiness": "medium",
            "overall_readiness": "medium"
        }
    
    def _calculate_leverage_impact(self, credit_amount: float, assets: float, base_risk: float) -> float:
        """Calcular impacto del apalancamiento"""
        leverage_ratio = credit_amount / assets
        if leverage_ratio > 0.5:
            return 10  # Aumenta el riesgo
        elif leverage_ratio > 0.3:
            return 5
        else:
            return -2  # Mejora ligeramente el score por acceso a capital
    
    def _calculate_credit_readiness(self, base_risk: float, financial_data: Dict) -> float:
        """Calcular preparación crediticia"""
        readiness = 100 - base_risk  # Score inverso al riesgo
        return max(0, min(100, readiness))
    
    def _calculate_diversification_benefit(self, revenue_increase: float, base_risk: float) -> float:
        """Calcular beneficio de diversificación"""
        return (revenue_increase / 100) * 8  # Reducción de riesgo por diversificación
    
    def _calculate_investment_risk(self, investment: float, revenue: float, base_risk: float) -> float:
        """Calcular riesgo de inversión"""
        investment_ratio = investment / revenue
        return investment_ratio * 20  # Aumento de riesgo por inversión
    
    def _assess_expansion_readiness(self, company_data: Dict, financial_data: Dict) -> str:
        """Evaluar preparación para expansión"""
        return "medium"  # Simplificado
    
    def _recommend_expansion_strategy(self, scenarios: Dict, base_risk: float) -> str:
        """Recomendar estrategia de expansión"""
        if base_risk < 60:
            return "Expansión agresiva recomendada"
        else:
            return "Expansión conservadora recomendada"
    
    def _calculate_sector_crisis_impact(self, financial_data: Dict) -> float:
        """Calcular impacto de crisis sectorial"""
        return -25  # Impacto promedio del 25%
    
    def _calculate_financial_stress_impact(self, revenue_impact: float, cost_increase: float, base_risk: float) -> float:
        """Calcular impacto de estrés financiero"""
        stress_factor = abs(revenue_impact) + cost_increase
        return stress_factor * 0.5  # Cada punto de estrés aumenta 0.5 puntos de riesgo
    
    def _assess_financial_flexibility(self, financial_data: Dict) -> str:
        """Evaluar flexibilidad financiera"""
        return "medium"  # Simplificado
    
    def _generate_shock_preparedness_recommendations(self, scenarios: Dict, cash_reserves: float, revenue: float) -> List[str]:
        """Generar recomendaciones de preparación para shocks"""
        recommendations = []
        
        cash_months = cash_reserves / (revenue / 12)
        
        if cash_months < 3:
            recommendations.append("Incrementar reservas de efectivo a mínimo 3 meses de gastos")
        
        if cash_months < 6:
            recommendations.append("Establecer línea de crédito de emergencia")
        
        recommendations.append("Diversificar proveedores y clientes")
        recommendations.append("Crear plan de contingencia operativo")
        
        return recommendations
