import { useEffect, useState } from 'react';
import RiskLevelChart from '../components/RiskLevelChart';
import SectorChart from '../components/SectorChart';
import StatsCard from '../components/StatsCard';
import { dashboardApi } from '../services/apiServices';
import { DashboardData } from '../types';

// Iconos para el dashboard
const IconChart = ({ className }: { className?: string }) => (
  <span className={`inline-block ${className}`} style={{ fontSize: '1.5em' }}>📊</span>
);

const IconGroup = ({ className }: { className?: string }) => (
  <span className={`inline-block ${className}`} style={{ fontSize: '1.5em' }}>👥</span>
);

const IconDocument = ({ className }: { className?: string }) => (
  <span className={`inline-block ${className}`} style={{ fontSize: '1.5em' }}>📋</span>
);

const IconWarning = ({ className }: { className?: string }) => (
  <span className={`inline-block ${className}`} style={{ fontSize: '1.5em' }}>⚠️</span>
);

const IconDollar = ({ className }: { className?: string }) => (
  <span className={`inline-block ${className}`} style={{ fontSize: '1.5em' }}>💰</span>
);

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
      console.error('Error loading dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-500"></div>
      </div>
    );
  }

  if (!dashboardData) {
    return (
      <div className="text-center py-12">
        <IconWarning className="mx-auto h-12 w-12 text-gray-400" />
        <h3 className="mt-2 text-sm font-medium text-gray-900">No se pudieron cargar los datos</h3>
        <p className="mt-1 text-sm text-gray-500">
          Intenta recargar la página o contacta al administrador.
        </p>
      </div>
    );
  }

  const approvalRate = dashboardData.total_applications > 0 
    ? (dashboardData.approved_applications / dashboardData.total_applications * 100).toFixed(1)
    : '0';

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-2 text-sm text-gray-700">
          Resumen general del sistema de evaluación de riesgo financiero para PYMEs
        </p>
      </div>

      {/* Tarjetas de estadísticas */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
        <StatsCard
          title="Total Solicitudes"
          value={dashboardData.total_applications.toString()}
          icon={IconDocument}
          color="blue"
        />
        <StatsCard
          title="Tasa de Aprobación"
          value={`${approvalRate}%`}
          icon={IconChart}
          color="green"
        />
        <StatsCard
          title="Score Promedio"
          value={dashboardData.average_risk_score.toFixed(1)}
          icon={IconGroup}
          color="yellow"
        />
        <StatsCard
          title="Crédito Total"
          value={`$${(dashboardData.total_credit_amount / 1000000).toFixed(1)}M`}
          icon={IconDollar}
          color="purple"
        />
      </div>

      {/* Estado de solicitudes */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Estado de Solicitudes</h3>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Aprobadas</span>
              <div className="flex items-center">
                <span className="badge badge-success">{dashboardData.approved_applications}</span>
              </div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Pendientes</span>
              <div className="flex items-center">
                <span className="badge badge-warning">{dashboardData.pending_applications}</span>
              </div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Rechazadas</span>
              <div className="flex items-center">
                <span className="badge badge-danger">{dashboardData.rejected_applications}</span>
              </div>
            </div>
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Distribución de Riesgo</h3>
          <RiskLevelChart data={dashboardData.risk_level_distribution} />
        </div>

        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Sectores Principales</h3>
          <SectorChart data={dashboardData.sector_distribution} />
        </div>
      </div>

      {/* Actividad reciente */}
      <div className="card">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Actividad Reciente</h3>
        <div className="text-sm text-gray-500">
          Esta sección mostraría las actividades más recientes del sistema, como nuevas solicitudes, 
          análisis completados, etc.
        </div>
      </div>
    </div>
  );
}
