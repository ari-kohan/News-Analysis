import React, { useState } from 'react';
import { Newspaper } from 'lucide-react';
import { SearchBar } from './components/SearchBar';
import { ArticleCard } from './components/ArticleCard';
import { ArticleModal } from './components/ArticleModal';
// import { AdminPanel } from './components/AdminPanel';
import { Article, SearchFilters } from './types';
import { useArticles } from './hooks/useArticles';
import { TagProvider, useTag } from './contexts/TagContext';

function AppContent() {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchFilters, setSearchFilters] = useState<SearchFilters>({});
  const [selectedArticle, setSelectedArticle] = useState<Article | null>(null);
  const { selectedTag } = useTag();

  const { articles, loading, error } = useArticles(searchQuery, {
    ...searchFilters,
    tag: selectedTag,
  });

  const handleSearch = (query: string, filters: SearchFilters) => {
    setSearchQuery(query);
    setSearchFilters(filters);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Newspaper className="text-blue-600" size={32} />
              <h1 className="text-2xl font-bold text-gray-900">
                NewsAggregator
              </h1>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <div className="mb-8">
          <SearchBar onSearch={handleSearch} />
          {selectedTag && (
            <div className="mt-4">
              <p className="text-sm text-gray-600">
                Filtering by tag:{' '}
                <span className="font-medium">{selectedTag}</span>
              </p>
            </div>
          )}
        </div>

        {error && (
          <div className="mb-8 p-4 bg-red-50 text-red-700 rounded-lg">
            {error}
          </div>
        )}

        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {articles.map((article) => (
              <ArticleCard
                key={article.id}
                article={article}
                onClick={setSelectedArticle}
              />
            ))}
          </div>
        )}

        {selectedArticle && (
          <ArticleModal
            article={selectedArticle}
            onClose={() => setSelectedArticle(null)}
          />
        )}
      </main>

      {/* <AdminPanel /> */}
    </div>
  );
}

function App() {
  return (
    <TagProvider>
      <AppContent />
    </TagProvider>
  );
}

export default App;