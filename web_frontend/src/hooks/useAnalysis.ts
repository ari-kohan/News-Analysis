import { useState, useEffect, useCallback } from 'react';
import { fetchAllArticles, searchArticles } from '../services/analysisService';
import { logger } from '../utils/logger';
import { SearchFilters } from '../types';
import { GetAllArticlesData } from '@firebasegen/news-connector';

export function useAnalysis(query: string = '', filters: SearchFilters = {}) {
  const [articles, setArticles] = useState<GetAllArticlesData>();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadArticles = useCallback(async () => {
    logger.info(query ? `Searching articles with query: ${query}` : 'Loading all articles...');
    try {
      setLoading(true);
      setError(null);
      const data = query ? await searchArticles(query) : await fetchAllArticles();
      if (!data) {
        throw new Error('Failed to fetch articles');
      }
      logger.info(`Successfully loaded ${data.articleAnalyses.length} articles`);
      setArticles(data);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch articles';
      logger.error('Error loading articles:', err);
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadArticles().catch(err => {
      logger.error('Failed to load analyses in effect:', err);
      setError('Failed to load analyses. Please try again later.');
    });
  }, [loadArticles]);

  return { articles, loading, error };
}