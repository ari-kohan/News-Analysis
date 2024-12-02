import React from 'react';
import { Calendar, Globe } from 'lucide-react';
import { Article } from '../types';

interface ArticleCardProps {
  article: Article;
  onClick: (article: Article) => void;
}

export function ArticleCard({ article, onClick }: ArticleCardProps) {
  return (
    <div
      className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200 cursor-pointer"
      onClick={() => onClick(article)}
    >
      <div className="p-4">
        <h2 className="text-xl font-semibold mb-2 line-clamp-2">
          {article.title}
        </h2>
        <p className="text-gray-600 mb-4 line-clamp-3">
          {article.content.substring(0, 200)}...
        </p>

        <div className="flex items-center justify-between text-sm text-gray-500">
          <div className="flex items-center gap-1">
            <Globe size={14} />
            <a
              href={article.link}
              target="_blank"
              rel="noopener noreferrer"
              onClick={(e) => e.stopPropagation()}
              className="hover:text-blue-600"
            >
              {article.source}
            </a>
          </div>
          <div className="flex items-center gap-1">
            <Calendar size={14} />
            <span>{new Date(article.date).toLocaleDateString()}</span>
          </div>
        </div>

        {article.authors.length > 0 && (
          <div className="mt-2 text-sm text-gray-500">By {article.authors}</div>
        )}
      </div>
    </div>
  );
}
