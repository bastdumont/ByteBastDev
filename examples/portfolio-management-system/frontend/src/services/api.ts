import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Stock API
export const stockApi = {
  getQuote: async (symbol: string) => {
    const response = await api.get(`/stocks/quote/${symbol}`);
    return response.data;
  },

  getInfo: async (symbol: string) => {
    const response = await api.get(`/stocks/info/${symbol}`);
    return response.data;
  },

  getHistory: async (symbol: string, period: string = '1mo', interval: string = '1d') => {
    const response = await api.get(`/stocks/history/${symbol}`, {
      params: { period, interval }
    });
    return response.data.data;
  },

  search: async (query: string) => {
    const response = await api.get('/stocks/search', {
      params: { q: query }
    });
    return response.data.results;
  },
};

// Portfolio API
export const portfolioApi = {
  getAll: async () => {
    const response = await api.get('/portfolios');
    return response.data;
  },

  getById: async (id: string) => {
    const response = await api.get(`/portfolios/${id}`);
    return response.data;
  },

  create: async (data: { name: string; description?: string }) => {
    const response = await api.post('/portfolios', data);
    return response.data;
  },

  update: async (id: string, data: any) => {
    const response = await api.put(`/portfolios/${id}`, data);
    return response.data;
  },

  delete: async (id: string) => {
    await api.delete(`/portfolios/${id}`);
  },

  addHolding: async (id: string, holding: any) => {
    const response = await api.post(`/portfolios/${id}/holdings`, holding);
    return response.data;
  },

  removeHolding: async (id: string, symbol: string) => {
    const response = await api.delete(`/portfolios/${id}/holdings/${symbol}`);
    return response.data;
  },

  refresh: async (id: string) => {
    const response = await api.post(`/portfolios/${id}/refresh`);
    return response.data;
  },

  getMetrics: async (id: string) => {
    const response = await api.get(`/portfolios/${id}/metrics`);
    return response.data;
  },
};

export default api;
