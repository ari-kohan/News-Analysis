import { handleGetArticleById, handleGetAllArticles, handleSearchArticles } from '../lib/ArticleService';

// Fetch all articles
export const fetchAllArticles = async () => {
  return await handleGetAllArticles();
};

// Fetch article by ID
export const fetchArticleById = async (articleId: string) => {
  return await handleGetArticleById(articleId);
};

// Search articles for a query
export const searchArticles = async (query: string) => {
  return await handleSearchArticles(query);
};


