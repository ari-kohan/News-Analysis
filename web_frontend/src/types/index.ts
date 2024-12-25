import { TimestampString } from "@firebasegen/news-connector";
import { Timestamp } from "firebase/firestore";

export interface FullArticle {
  id: string;
  title: string;
  content: string;
  date: Timestamp;
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

// export interface ArticleAnalysis {
//   id: string;
//   summary?: string | null;
//   people?: string[] | null;
//   places?: string[] | null;
//   agencies?: string[] | null;
//   laws?: string[] | null;
//   climate?: string[] | null;
//   tags?: string[] | null;
// }

// export interface Article {
//   id: string;
//   title: string;
//   date: TimestampString
//   source: string;
//   link: string;
//   authors: string[];
// }
