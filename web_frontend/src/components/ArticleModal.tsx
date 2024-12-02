import React from 'react';
import { X, Globe, Calendar, Users } from 'lucide-react';
import { Article } from '../types';

interface ArticleModalProps {
  article: Article;
  onClose: () => void;
}

export function ArticleModal({ article, onClose }: ArticleModalProps) {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-white border-b border-gray-200 p-4 flex items-center justify-between">
          <h2 className="text-2xl font-semibold">{article.title}</h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
            <X size={24} />
          </button>
        </div>

        <div className="p-6">
          <div className="flex items-center gap-4 text-sm text-gray-600 mb-4">
            <div className="flex items-center gap-1">
              <Globe size={16} />
              <a
                href={article.link}
                target="_blank"
                rel="noopener noreferrer"
                className="hover:text-blue-600"
              >
                {article.source}
              </a>
            </div>
            <div className="flex items-center gap-1">
              <Calendar size={16} />
              <span>{new Date(article.date).toLocaleDateString()}</span>
            </div>
            {article.authors.length > 0 && (
              <div className="flex items-center gap-1">
                <Users size={16} />
                <span>{article.authors}</span>
              </div>
            )}
          </div>

          <div className="prose max-w-none">
            <div className="whitespace-pre-wrap">{article.content}</div>
          </div>
        </div>
      </div>
    </div>
  );
}
