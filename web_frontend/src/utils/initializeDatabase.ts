import { collection, addDoc, Timestamp } from 'firebase/firestore';
import { db } from '../config/firebase';

const sampleArticles = [
  {
    title: "AI Breakthrough in Climate Research",
    summary: "Scientists leverage artificial intelligence to predict climate patterns with unprecedented accuracy.",
    content: "In a groundbreaking development, researchers have successfully implemented advanced AI algorithms to analyze climate data...",
    publishedAt: Timestamp.fromDate(new Date()),
    source: "TechScience Daily",
    url: "https://example.com/ai-climate-research",
    imageUrl: "https://images.unsplash.com/photo-1451187580459-43490279c0fa",
    tags: ["AI", "Climate Change", "Research"],
    topics: ["Technology", "Environment"],
    people: ["Dr. Sarah Johnson", "Prof. Michael Chen"],
    searchableText: ["ai", "climate", "research", "technology", "environment"]
  },
  {
    title: "Global Economic Forum Addresses Tech Innovation",
    summary: "World leaders gather to discuss the impact of emerging technologies on global economics.",
    content: "The annual Global Economic Forum commenced today with a focus on technological innovation...",
    publishedAt: Timestamp.fromDate(new Date(Date.now() - 86400000)), // 1 day ago
    source: "World Economics Review",
    url: "https://example.com/economic-forum-tech",
    imageUrl: "https://images.unsplash.com/photo-1444653614773-995cb1ef9efa",
    tags: ["Economics", "Technology", "Innovation"],
    topics: ["Business", "Technology"],
    people: ["Jane Smith", "Robert Williams"],
    searchableText: ["economics", "technology", "innovation", "business"]
  }
];

export async function initializeDatabase() {
  try {
    const articlesRef = collection(db, 'articles');
    
    for (const article of sampleArticles) {
      await addDoc(articlesRef, article);
    }
    
    console.log('Sample articles added successfully');
    return true;
  } catch (error) {
    console.error('Error initializing database:', error);
    return false;
  }
}