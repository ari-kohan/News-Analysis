import { collection, addDoc, getDocs, query, limit } from 'firebase/firestore';
import { db } from '../config/firebase';
import { logger } from './logger';

const sampleArticles = [
  {
    title: 'AI Breakthrough in Climate Research',
    content:
      'Scientists have made significant progress in applying artificial intelligence to climate research. The new methods allow for more accurate predictions and better understanding of climate patterns.',
    date: new Date().toISOString(),
    source: 'TechScience Daily',
    link: 'https://example.com/ai-climate-research',
    authors: ['Dr. Sarah Johnson', 'Prof. Michael Chen'],
  },
  {
    title: 'Global Economic Forum Addresses Tech Innovation',
    content:
      'The annual Global Economic Forum commenced today with a focus on technological innovation. Leaders from around the world gathered to discuss the impact of emerging technologies on the global economy.',
    date: new Date(Date.now() - 86400000).toISOString(), // 1 day ago
    source: 'World Economics Review',
    link: 'https://example.com/economic-forum-tech',
    authors: ['Jane Smith', 'Robert Williams'],
  },
];

export async function initializeDatabase() {
  try {
    logger.info('Checking Firebase connection...');
    const articlesRef = collection(db, 'test');

    // Test the connection by attempting to read
    try {
      const testQuery = query(articlesRef, limit(1));
      await getDocs(testQuery);
      logger.info('Firebase connection successful');
    } catch (error) {
      logger.error('Firebase connection test failed:', error);
      return false;
    }

    // Check if articles already exist
    const snapshot = await getDocs(articlesRef);
    logger.info(`Current articles count: ${snapshot.size}`);

    if (!snapshot.empty) {
      logger.info('Articles collection already contains data');
      return true;
    }

    logger.info('Adding sample articles to database...');
    for (const article of sampleArticles) {
      const docRef = await addDoc(articlesRef, article);
      logger.debug('Added article with ID:', docRef.id);
    }

    logger.info('Sample articles added successfully');
    return true;
  } catch (error) {
    logger.error('Error initializing database:', error);
    return false;
  }
}