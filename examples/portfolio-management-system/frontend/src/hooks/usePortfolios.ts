import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { portfolioApi } from '../services/api';
import { Portfolio, CreatePortfolioRequest, AddHoldingRequest } from '../types';

// Fetch all portfolios
export const usePortfolios = () => {
  return useQuery<Portfolio[]>({
    queryKey: ['portfolios'],
    queryFn: portfolioApi.getAll,
    staleTime: 30000, // Consider data fresh for 30 seconds
  });
};

// Fetch single portfolio
export const usePortfolio = (portfolioId: string | undefined) => {
  return useQuery<Portfolio>({
    queryKey: ['portfolio', portfolioId],
    queryFn: () => portfolioApi.getById(portfolioId!),
    enabled: !!portfolioId, // Only run query if portfolioId exists
    staleTime: 30000,
  });
};

// Create portfolio mutation
export const useCreatePortfolio = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreatePortfolioRequest) => portfolioApi.create(data),
    onSuccess: () => {
      // Invalidate portfolios list to refetch
      queryClient.invalidateQueries({ queryKey: ['portfolios'] });
    },
  });
};

// Update portfolio mutation
export const useUpdatePortfolio = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<Portfolio> }) =>
      portfolioApi.update(id, data),
    onSuccess: (_, variables) => {
      // Invalidate both the list and the specific portfolio
      queryClient.invalidateQueries({ queryKey: ['portfolios'] });
      queryClient.invalidateQueries({ queryKey: ['portfolio', variables.id] });
    },
  });
};

// Delete portfolio mutation
export const useDeletePortfolio = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (portfolioId: string) => portfolioApi.delete(portfolioId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['portfolios'] });
    },
  });
};

// Add holding mutation
export const useAddHolding = (portfolioId: string) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: AddHoldingRequest) =>
      portfolioApi.addHolding(portfolioId, data),
    onSuccess: () => {
      // Invalidate to refetch with new holding
      queryClient.invalidateQueries({ queryKey: ['portfolio', portfolioId] });
      queryClient.invalidateQueries({ queryKey: ['portfolios'] });
      queryClient.invalidateQueries({ queryKey: ['metrics', portfolioId] });
    },
  });
};

// Remove holding mutation
export const useRemoveHolding = (portfolioId: string) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (symbol: string) =>
      portfolioApi.removeHolding(portfolioId, symbol),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['portfolio', portfolioId] });
      queryClient.invalidateQueries({ queryKey: ['portfolios'] });
      queryClient.invalidateQueries({ queryKey: ['metrics', portfolioId] });
    },
  });
};

// Refresh portfolio prices
export const useRefreshPortfolio = (portfolioId: string) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: () => portfolioApi.refresh(portfolioId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['portfolio', portfolioId] });
      queryClient.invalidateQueries({ queryKey: ['metrics', portfolioId] });
    },
  });
};

// Fetch portfolio metrics
export const usePortfolioMetrics = (portfolioId: string | undefined) => {
  return useQuery({
    queryKey: ['metrics', portfolioId],
    queryFn: () => portfolioApi.getMetrics(portfolioId!),
    enabled: !!portfolioId,
    staleTime: 30000,
  });
};
