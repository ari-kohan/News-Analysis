import { getAllArticles, GetArticleByIdData, getArticleById, addArticle, deleteArticle, TimestampString, GetAllArticlesData, searchArticles } from '@firebasegen/news-connector';
import { ConnectorConfig, DataConnect, QueryRef, QueryPromise } from 'firebase/data-connect';
import { dataconnect } from '../config/firebase';

// // Fetch articles with pagination and filters
// export const handleGetArticles = async (
//   limit: number,
//   offset: number,
//   filters?: { tag?: string; searchQuery?: string }
// ): Promise<AddArticleData["articles"] | null> => {
//   try {
//     const response = await getArticleById({ 
//       limit,
//       offset,
//       ...filters
//     });
//     return response.data.articles;
//   } catch (error) {
//     console.error("Error fetching articles:", error);
//     return null;
//   }
// };

// Fetch single article by ID
export const handleGetArticleById = async (
  articleId: string
): Promise<GetArticleByIdData["article"] | null> => {
  try {
    const response = await getArticleById({ id: articleId });
    if (response.data.article) {
      return response.data.article;
    }
    return null;
  } catch (error) {
    console.error("Error fetching article:", error);
    return null;
  }
};

// Add new article
export const handleAddArticle = async (
  articleData: {
    id: string;
    title: string;
    date: TimestampString;
    authors: string[];
    source: string;
    link: string;
  }
): Promise<void> => {
  try {
    await addArticle(articleData);
  } catch (error) {
    console.error("Error adding article:", error);
    throw error;
  }
};

// // Update existing article
// export const handleUpdateArticle = async (
//   articleId: string,
//   updateData: Partial<{
//     title?: string;
//     date?: TimestampString;
//     authors?: string[];
//     source?: string;
//     link?: string;
//   }>
// ): Promise<void> => {
//   try {
//     await updateArticle({ id: articleId, ...updateData });
//   } catch (error) {
//     console.error("Error updating article:", error);
//     throw error;
//   }
// };

// Delete article
export const handleDeleteArticle = async (
  articleId: string
): Promise<void> => {
  try {
    await deleteArticle({ id: articleId });
  } catch (error) {
    console.error("Error deleting article:", error);
    throw error;
  }
};

export const handleGetAllArticles = async (): Promise<GetAllArticlesData | null> => {
  try {
    const response = await getAllArticles(dataconnect);
    return response.data;
  } catch (error) {
    console.error("Error fetching articles:", error);
    return null;
  }
};

export const handleSearchArticles = async (query: string): Promise<GetAllArticlesData | null> => {
  try {
    const response = await searchArticles(dataconnect, { query });
    return response.data;
  } catch (error) {
    console.error("Error searching articles:", error);
    return null;
  }
};

