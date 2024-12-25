import { collection, query, getDocs, where, orderBy, QueryConstraint, limit } from 'firebase/firestore';
import { db } from '../config/firebase';
import { FullArticle, SearchFilters } from '../types';
import { logger } from '../utils/logger';

export async function fetchArticles(searchQuery?: string, filters?: SearchFilters): Promise<FullArticle[]> {
  logger.info('Fetching articles with query:', { searchQuery, filters });
  
  try {
    const articlesRef = collection(db, 'articles');
    logger.debug('Articles collection reference:', articlesRef.path);
    
    // First, check if the collection exists and has documents
    const checkSnapshot = await getDocs(query(articlesRef, limit(1)));
    logger.debug('Collection check result:', {
      exists: !checkSnapshot.empty,
      size: checkSnapshot.size
    });

    if (checkSnapshot.empty) {
      logger.warn('Articles collection is empty');
      return [];
    }

    const constraints: QueryConstraint[] = [orderBy('date', 'desc')];

    if (searchQuery) {
      constraints.push(where('content', '>=', searchQuery.toLowerCase()));
    }

    if (filters?.dateFrom) {
      constraints.push(where('date', '>=', filters.dateFrom));
    }

    if (filters?.dateTo) {
      constraints.push(where('date', '<=', filters.dateTo));
    }

    const q = query(articlesRef, ...constraints);
    logger.debug('Query path:', q);

    const querySnapshot = await getDocs(q);
    logger.info(`Retrieved ${querySnapshot.size} articles from Firebase`);
    
    const articles = querySnapshot.docs.map(doc => {
      const data = doc.data();
      logger.debug('Document data:', { id: doc.id, data });
      return {
        id: doc.id,
        title: data.title || '',
        content: data.content || '',
        date: data.date || new Date().toISOString(),
        source: data.source || '',
        link: data.link || '',
        authors: data.authors || []
      } as FullArticle;
    });

    return articles;
  } catch (error) {
    logger.error('Error fetching articles:', error);
    throw new Error('Failed to fetch articles. Please check your Firebase configuration and network connection.');
  }
}