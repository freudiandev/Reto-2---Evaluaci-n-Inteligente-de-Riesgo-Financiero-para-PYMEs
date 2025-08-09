import api from './api';
import type {
  Company,
  CompanyCreate,
  CreditApplication,
  CreditApplicationCreate,
  FinancialStatement,
  SocialMediaAnalysis,
  SocialMediaAnalysisRequest,
  RiskScore,
  SimulationScenario,
  SimulationRequest,
  DashboardData,
  RiskAnalysisReport,
} from '../types';

// Companies API
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

// Credit Applications API
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

// Financial Statements API
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

// Social Media Analysis API
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

// Risk Score API
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

// Simulations API
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

// Dashboard API
export const dashboardApi = {
  getSummary: async (): Promise<DashboardData> => {
    const response = await api.get('/dashboard/summary');
    return response.data;
  },
};

// Reports API
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

// Health Check
export const healthApi = {
  check: async () => {
    const response = await api.get('/health');
    return response.data;
  },
};
