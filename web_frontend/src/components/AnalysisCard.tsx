import React from 'react';
import { Calendar, Globe } from 'lucide-react';
import { GetArticleAnalysisByIdData } from '@firebasegen/news-connector';

interface AnalysisCardProps {
  analysis: any;
  onClick: (analysis: any) => void;
}

export function AnalysisCard({ analysis, onClick }: AnalysisCardProps) {
  return (
    <div
      className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200 cursor-pointer"
      onClick={() => onClick(analysis)}
    >
      <div className="p-4">
        <h2 className="text-xl font-semibold mb-2 line-clamp-2">
          {analysis.article.title}
        </h2>
        <p className="text-gray-600 mb-4 line-clamp-3">
          {analysis.summary?.substring(0, 200)}...
        </p>

        <div className="flex items-center justify-between text-sm text-gray-500">
          <div className="flex items-center gap-1">
            <Globe size={14} />
            <a
              href={analysis.article.link}
              target="_blank"
              rel="noopener noreferrer"
              onClick={(e) => e.stopPropagation()}
              className="hover:text-blue-600"
            >
              {analysis.article.source}
            </a>
          </div>
          <div className="flex items-center gap-1">
            <Calendar size={14} />
            <span>{new Date(analysis.article.date).toLocaleDateString()}</span>
          </div>
        </div>

        {analysis.article.authors?.length > 0 && (
          <div className="mt-2 text-sm text-gray-500">By {analysis.article.authors}</div>
        )}
      </div>
    </div>
  );
}
