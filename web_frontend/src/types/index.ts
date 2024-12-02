export interface Article {
  id: string;
  title: string;
  content: string;
  date: string;
  source: string;
  link: string;
  authors: string[];
}

export interface SearchFilters {
  topic?: string;
  person?: string;
  source?: string;
  dateFrom?: string;
  dateTo?: string;
  tag?: string | null;
}