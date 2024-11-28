import { collection, query, getDocs, where, orderBy, QueryConstraint } from 'firebase/firestore';
import { db } from '../config/firebase';
import { Article, SearchFilters } from '../types';

export async function fetchArticles(searchQuery?: string, filters?: SearchFilters): Promise<Article[]> {
  const articlesRef = collection(db, 'articles');
  const constraints: QueryConstraint[] = [orderBy('publishedAt', 'desc')];

  if (searchQuery) {
    constraints.push(where('searchableText', 'array-contains', searchQuery.toLowerCase()));
  }

  if (filters?.topic) {
    constraints.push(where('topics', 'array-contains', filters.topic));
  }

  if (filters?.person) {
    constraints.push(where('people', 'array-contains', filters.person));
  }

  if (filters?.tag) {
    constraints.push(where('tags', 'array-contains', filters.tag));
  }

  if (filters?.dateFrom) {
    constraints.push(where('publishedAt', '>=', filters.dateFrom));
  }

  if (filters?.dateTo) {
    constraints.push(where('publishedAt', '<=', filters.dateTo));
  }

  const q = query(articlesRef, ...constraints);
  const querySnapshot = await getDocs(q);
  
  return querySnapshot.docs.map(doc => ({
    id: doc.id,
    ...doc.data()
  } as Article));
}