export interface Article {
  id: string;
  title: string;
  summary: string;
  content: string;
  publishedAt: string;
  source: string;
  url: string;
  imageUrl?: string;
  tags: string[];
  topics: string[];
  people: string[];
}

export interface SearchFilters {
  topic?: string;
  person?: string;
  source?: string;
  dateFrom?: string;
  dateTo?: string;
  tag?: string | null;
}