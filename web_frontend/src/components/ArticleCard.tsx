import React from 'react';
import { Calendar, Globe } from 'lucide-react';
import { Article } from '../types';
import { Tag } from './Tag';

interface ArticleCardProps {
  article: Article;
  onClick: (article: Article) => void;
}

export function ArticleCard({ article, onClick }: ArticleCardProps) {
  const handleClick = (e: React.MouseEvent) => {
    // Prevent opening the article when clicking on a tag
    if (!(e.target as HTMLElement).closest('button')) {
      onClick(article);
    }
  };

  return (
    <div 
      className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200 cursor-pointer"
      onClick={handleClick}
    >
      {article.imageUrl && (
        <img 
          src={article.imageUrl} 
          alt={article.title}
          className="w-full h-48 object-cover rounded-t-lg"
        />
      )}
      <div className="p-4">
        <h2 className="text-xl font-semibold mb-2 line-clamp-2">{article.title}</h2>
        <p className="text-gray-600 mb-4 line-clamp-3">{article.summary}</p>
        
        <div className="flex flex-wrap gap-2 mb-3">
          {article.tags.map((tag) => (
            <Tag key={tag} tag={tag} />
          ))}
        </div>
        
        <div className="flex items-center justify-between text-sm text-gray-500">
          <div className="flex items-center gap-1">
            <Globe size={14} />
            <span>{article.source}</span>
          </div>
          <div className="flex items-center gap-1">
            <Calendar size={14} />
            <span>{new Date(article.publishedAt).toLocaleDateString()}</span>
          </div>
        </div>
      </div>
    </div>
  );
}