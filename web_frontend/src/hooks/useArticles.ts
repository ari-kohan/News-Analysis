import { useState, useEffect, useCallback } from 'react';
import { FullArticle, SearchFilters } from '../types';
import { fetchArticles } from '../services/articleService';
import { logger } from '../utils/logger';

export function useArticles(searchQuery: string = '', filters: SearchFilters = {}) {
  const [articles, setArticles] = useState<FullArticle[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadArticles = useCallback(async () => {
    logger.info('Loading articles with:', { searchQuery, filters });
    try {
      setLoading(true);
      setError(null);
      const data = await fetchArticles(searchQuery, filters);
      logger.info(`Successfully loaded ${data.length} articles`);
      setArticles(data);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch articles';
      logger.error('Error loading articles:', err);
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  }, [searchQuery, JSON.stringify(filters)]);

  useEffect(() => {
    loadArticles().catch(err => {
      logger.error('Failed to load articles in effect:', err);
      setError('Failed to load articles. Please try again later.');
    });
  }, [loadArticles]);

  return { articles, loading, error };
}