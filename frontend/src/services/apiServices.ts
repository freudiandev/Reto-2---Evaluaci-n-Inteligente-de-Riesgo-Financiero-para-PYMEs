import axios from 'axios';
import type {
  Company,
  CompanyCreate,
  CreditApplication,
  CreditApplicationCreate,
  DashboardData,
  FinancialStatement,
  RiskAnalysisReport,
  RiskScore,
  SimulationRequest,
  SimulationScenario,
  SocialMediaAnalysis,
  SocialMediaAnalysisRequest,
} from '../types';
import api from './api';

// Cliente especial para endpoints v2 del hackathon
const v2Api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8001/api/v2',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Servicios para manejar empresas
export const companiesApi = {
  getAll: async (skip = 0, limit = 100) => {
    const response = await api.get(`/companies/?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  getById: async (id: number): Promise<Company> => {
    const response = await api.get(`/companies/${id}`);
    return response.data;
  },

  getByRuc: async (ruc: string): Promise<Company> => {
    const response = await api.get(`/companies/ruc/${ruc}`);
    return response.data;
  },

  create: async (company: CompanyCreate): Promise<Company> => {
    const response = await api.post('/companies/', company);
    return response.data;
  },

  update: async (id: number, company: Partial<CompanyCreate>): Promise<Company> => {
    const response = await api.put(`/companies/${id}`, company);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/companies/${id}`);
  },
};

// Solicitudes de crédito
export const applicationsApi = {
  getAll: async (skip = 0, limit = 100): Promise<CreditApplication[]> => {
    const response = await api.get(`/applications/?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  getById: async (id: number): Promise<CreditApplication> => {
    const response = await api.get(`/applications/${id}`);
    return response.data;
  },

  create: async (application: CreditApplicationCreate): Promise<CreditApplication> => {
    const response = await api.post('/applications/', application);
    return response.data;
  },

  updateStatus: async (id: number, status: string): Promise<CreditApplication> => {
    const response = await api.patch(`/applications/${id}`, { status });
    return response.data;
  },
};

// Estados financieros
export const financialStatementsApi = {
  uploadFile: async (
    companyId: number,
    applicationId: number,
    year: number,
    file: File
  ) => {
    const formData = new FormData();
    formData.append('company_id', companyId.toString());
    formData.append('application_id', applicationId.toString());
    formData.append('year', year.toString());
    formData.append('file', file);

    const response = await api.post('/financial-statements/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  create: async (statement: Partial<FinancialStatement>): Promise<FinancialStatement> => {
    const response = await api.post('/financial-statements/', statement);
    return response.data;
  },

  getByApplication: async (applicationId: number): Promise<FinancialStatement[]> => {
    const response = await api.get(`/financial-statements/application/${applicationId}`);
    return response.data;
  },
};

// Análisis de redes sociales
export const socialMediaApi = {
  analyze: async (request: SocialMediaAnalysisRequest) => {
    const response = await api.post('/social-media/analyze', request);
    return response.data;
  },

  getByApplication: async (applicationId: number): Promise<SocialMediaAnalysis[]> => {
    const response = await api.get(`/social-media/application/${applicationId}`);
    return response.data;
  },
};

// Cálculo de riesgo
export const riskScoreApi = {
  calculate: async (applicationId: number) => {
    const response = await api.post(`/risk-score/calculate/${applicationId}`);
    return response.data;
  },

  getByApplication: async (applicationId: number): Promise<RiskScore> => {
    const response = await api.get(`/risk-score/application/${applicationId}`);
    return response.data;
  },
};

// Simulaciones de escenarios
export const simulationsApi = {
  create: async (simulation: SimulationRequest): Promise<SimulationScenario> => {
    const response = await api.post('/simulations/', simulation);
    return response.data;
  },

  getByApplication: async (applicationId: number): Promise<SimulationScenario[]> => {
    const response = await api.get(`/simulations/application/${applicationId}`);
    return response.data;
  },
};

// Datos del dashboard
export const dashboardApi = {
  getSummary: async (): Promise<DashboardData> => {
    const response = await api.get('/dashboard/summary');
    return response.data;
  },
};

// Reportes y exportaciones
export const reportsApi = {
  getRiskAnalysis: async (applicationId: number): Promise<RiskAnalysisReport> => {
    const response = await api.get(`/reports/risk-analysis/${applicationId}`);
    return response.data;
  },

  exportPDF: async (applicationId: number): Promise<Blob> => {
    const response = await api.get(`/reports/export-pdf/${applicationId}`, {
      responseType: 'blob',
    });
    return response.data;
  },
};

// Estado del servidor
export const healthApi = {
  check: async () => {
    const response = await api.get('/health');
    return response.data;
  },
};

// ===============================
// NUEVOS SERVICIOS PARA HACKATHON
// ===============================

// Análisis integral del hackathon
export const hackathonApi = {
  // Análisis completo integrado
  comprehensiveAnalysis: async (request: {
    company_ruc: string;
    company_name: string;
    sector: string;
    social_media_urls?: string[];
    include_supercias_data?: boolean;
    include_digital_footprint?: boolean;
    include_scenario_analysis?: boolean;
  }) => {
    const response = await v2Api.post('/hackathon/comprehensive-analysis', request);
    return response.data;
  },

  // Búsqueda en Super de Compañías
  searchCompany: async (ruc: string) => {
    const response = await v2Api.get(`/hackathon/company-search/${ruc}`);
    return response.data;
  },

  // Análisis de huella digital
  digitalFootprintAnalysis: async (formData: FormData) => {
    const response = await v2Api.post('/hackathon/digital-footprint-analysis', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Simulaciones de escenarios
  scenarioSimulations: async (formData: FormData) => {
    const response = await v2Api.post('/hackathon/scenario-simulations', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Upload de documentos financieros
  uploadFinancialDocument: async (formData: FormData) => {
    const response = await v2Api.post('/hackathon/upload-financial-document', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Benchmarks sectoriales
  getSectorBenchmarks: async (sector: string) => {
    const response = await v2Api.get(`/hackathon/sector-benchmarks/${sector}`);
    return response.data;
  },

  // Datos de demostración
  getDemoData: async () => {
    const response = await v2Api.get('/hackathon/demo-data');
    return response.data;
  },
};

// Servicios RAG existentes actualizados
export const ragApi = {
  // Upload de documentos RAG
  uploadDocument: async (formData: FormData) => {
    const response = await api.post('/api/v2/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Análisis RAG completo
  comprehensiveAnalysis: async (request: {
    company_data: any;
    documents: any[];
  }) => {
    const response = await api.post('/api/v2/analysis/comprehensive', request);
    return response.data;
  },

  // Análisis de sentimiento
  sentimentAnalysis: async (ruc: string) => {
    const response = await api.get(`/api/v2/sentiment/${ruc}`);
    return response.data;
  },

  // Búsqueda semántica
  semanticSearch: async (query: string) => {
    const response = await api.post('/api/v2/documents/search', { query });
    return response.data;
  },

  // Análisis LLM directo
  llmAnalysis: async (request: {
    prompt: string;
    company_context?: any;
  }) => {
    const response = await api.post('/api/v2/llm/analyze', request);
    return response.data;
  },

  // Análisis sectorial
  sectorAnalysis: async (sector: string) => {
    const response = await api.get(`/api/v2/sector/analysis/${sector}`);
    return response.data;
  },

  // Estado del sistema RAG
  systemStatus: async () => {
    const response = await api.get('/api/v2/system/status');
    return response.data;
  },
};
