import { useState, useEffect, useCallback } from 'react';
import { Article, SearchFilters } from '../types';
import { fetchArticles } from '../services/articleService';

export function useArticles(searchQuery: string = '', filters: SearchFilters = {}) {
  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadArticles = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await fetchArticles(searchQuery, filters);
      setArticles(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch articles');
    } finally {
      setLoading(false);
    }
  }, [searchQuery, JSON.stringify(filters)]); // Stable dependency array

  useEffect(() => {
    loadArticles();
  }, [loadArticles]);

  return { articles, loading, error };
}