import { useEffect, useState } from 'react';
import RiskLevelChart from '../components/RiskLevelChart';
import SectorChart from '../components/SectorChart';
import { dashboardApi } from '../services/apiServices';
import { DashboardData } from '../types';

export default function Dashboard() {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const data = await dashboardApi.getSummary();
      setDashboardData(data);
    } catch (error) {
      console.error('Error cargando datos del dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <section className="cyberpunk-loading">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <h3 className="neon-text">Cargando datos del sistema...</h3>
          <div className="loading-grid"></div>
        </div>
      </section>
    );
  }

  if (!dashboardData) {
    return (
      <section className="error-section">
        <div className="error-container">
          <h3 className="error-title neon-text">⚠️ Error de conexión</h3>
          <p className="error-message glow-text">
            No se pudieron cargar los datos del sistema. Verifica la conexión con el backend.
          </p>
          <button className="btn-primary" onClick={loadDashboardData}>
            🔄 Reintentar
          </button>
        </div>
      </section>
    );
  }

  const approvalRate = dashboardData.total_applications > 0 
    ? (dashboardData.approved_applications / dashboardData.total_applications * 100).toFixed(1)
    : '0';

  return (
    <div className="dashboard-container">
      {/* Header del Dashboard */}
      <section className="dashboard-header">
        <h2 className="section-title neon-text">🎯 Centro de Control Financiero</h2>
        <p className="section-subtitle glow-text">
          Sistema de monitoreo en tiempo real para análisis de riesgo crediticio
        </p>
        <div className="cyber-divider"></div>
      </section>

      {/* Métricas principales */}
      <section className="metrics-grid">
        <div className="metric-card">
          <div className="metric-icon">📋</div>
          <div className="metric-value">{dashboardData.total_applications}</div>
          <div className="metric-label">Total Solicitudes</div>
          <div className="metric-glow pink"></div>
        </div>

        <div className="metric-card">
          <div className="metric-icon">✅</div>
          <div className="metric-value">{approvalRate}%</div>
          <div className="metric-label">Tasa Aprobación</div>
          <div className="metric-glow green"></div>
        </div>

        <div className="metric-card">
          <div className="metric-icon">📊</div>
          <div className="metric-value">{dashboardData.average_risk_score.toFixed(1)}</div>
          <div className="metric-label">Score Promedio</div>
          <div className="metric-glow blue"></div>
        </div>

        <div className="metric-card">
          <div className="metric-icon">💰</div>
          <div className="metric-value">${(dashboardData.total_credit_amount / 1000000).toFixed(1)}M</div>
          <div className="metric-label">Crédito Total</div>
          <div className="metric-glow purple"></div>
        </div>
      </section>

      {/* Análisis detallado */}
      <section className="analysis-grid">
        {/* Estado de solicitudes */}
        <div className="analysis-card">
          <h3 className="card-title neon-text">🔥 Estado de Solicitudes</h3>
          <div className="status-grid">
            <div className="status-item approved">
              <span className="status-icon">✅</span>
              <span className="status-value">{dashboardData.approved_applications}</span>
              <span className="status-label">Aprobadas</span>
            </div>
            <div className="status-item pending">
              <span className="status-icon">⏳</span>
              <span className="status-value">{dashboardData.pending_applications}</span>
              <span className="status-label">Pendientes</span>
            </div>
            <div className="status-item rejected">
              <span className="status-icon">❌</span>
              <span className="status-value">{dashboardData.rejected_applications}</span>
              <span className="status-label">Rechazadas</span>
            </div>
          </div>
        </div>

        {/* Distribución de riesgo */}
        <div className="analysis-card">
          <h3 className="card-title neon-text">⚡ Distribución de Riesgo</h3>
          <div className="chart-container">
            <RiskLevelChart data={dashboardData.risk_level_distribution} />
          </div>
        </div>

        {/* Sectores principales */}
        <div className="analysis-card">
          <h3 className="card-title neon-text">🏢 Sectores Principales</h3>
          <div className="chart-container">
            <SectorChart data={dashboardData.sector_distribution} />
          </div>
        </div>
      </section>

      {/* Actividad del sistema */}
      <section className="activity-section">
        <h3 className="section-title neon-text">🌐 Actividad del Sistema</h3>
        <div className="activity-grid">
          <div className="activity-card">
            <div className="activity-icon">🔄</div>
            <div className="activity-content">
              <h4 className="activity-title">Sistema Operativo</h4>
              <p className="activity-desc">
                Todos los servicios de análisis están funcionando correctamente
              </p>
            </div>
            <div className="activity-status active"></div>
          </div>
          
          <div className="activity-card">
            <div className="activity-icon">🤖</div>
            <div className="activity-content">
              <h4 className="activity-title">IA en Línea</h4>
              <p className="activity-desc">
                Modelos de machine learning listos para evaluaciones
              </p>
            </div>
            <div className="activity-status active"></div>
          </div>
          
          <div className="activity-card">
            <div className="activity-icon">💾</div>
            <div className="activity-content">
              <h4 className="activity-title">Base de Datos</h4>
              <p className="activity-desc">
                Conexión estable con {dashboardData.total_applications} registros
              </p>
            </div>
            <div className="activity-status active"></div>
          </div>
        </div>
      </section>
    </div>
  );
}
