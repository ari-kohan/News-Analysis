import { ConnectorConfig, DataConnect, QueryRef, QueryPromise, MutationRef, MutationPromise } from 'firebase/data-connect';
export const connectorConfig: ConnectorConfig;

export type TimestampString = string;

export type UUIDString = string;

export type Int64String = string;

export type DateString = string;



export interface AddArticleAnalysisData {
  articleAnalysis_insert: ArticleAnalysis_Key;
}

export interface AddArticleAnalysisVariables {
  articleId: UUIDString;
  summary?: string | null;
  people?: string[] | null;
  places?: string[] | null;
  agencies?: string[] | null;
  laws?: string[] | null;
  climate?: string[] | null;
  tags?: string[] | null;
}

export interface AddArticleData {
  article_insert: Article_Key;
}

export interface AddArticleVariables {
  id: UUIDString;
  title: string;
  date: TimestampString;
  authors?: string[] | null;
  source: string;
  link: string;
}

export interface ArticleAnalysis_Key {
  articleId: UUIDString;
  __typename?: 'ArticleAnalysis_Key';
}

export interface Article_Key {
  id: UUIDString;
  __typename?: 'Article_Key';
}

export interface DeleteArticleAnalysisData {
  articleAnalysis_delete?: ArticleAnalysis_Key | null;
}

export interface DeleteArticleAnalysisVariables {
  key?: ArticleAnalysis_Key | null;
}

export interface DeleteArticleData {
  article_delete?: Article_Key | null;
}

export interface DeleteArticleVariables {
  id: UUIDString;
}

export interface GetAllArticlesData {
  articleAnalyses: ({
    article: {
      id: UUIDString;
      title: string;
      date: TimestampString;
      source: string;
      link: string;
      authors: string[];
    } & Article_Key;
      articleId: UUIDString;
      summary?: string | null;
      people?: string[] | null;
      places?: string[] | null;
      agencies?: string[] | null;
      laws?: string[] | null;
      climate?: string[] | null;
      tags?: string[] | null;
  } & ArticleAnalysis_Key)[];
}

export interface GetArticleAnalysisByIdData {
  articleAnalysis?: {
    articleId: UUIDString;
    article: {
      id: UUIDString;
      authors: string[];
      date: TimestampString;
      link: string;
      source: string;
      title: string;
    } & Article_Key;
      agencies?: string[] | null;
      climate?: string[] | null;
      laws?: string[] | null;
      people?: string[] | null;
      places?: string[] | null;
      summary?: string | null;
      tags?: string[] | null;
  } & ArticleAnalysis_Key;
}

export interface GetArticleAnalysisByIdVariables {
  articleId: UUIDString;
}

export interface GetArticleByIdData {
  article?: {
    title: string;
    date: TimestampString;
    authors: string[];
    source: string;
    link: string;
    articleAnalysis?: {
      summary?: string | null;
      people?: string[] | null;
      places?: string[] | null;
      agencies?: string[] | null;
      laws?: string[] | null;
      climate?: string[] | null;
    };
  };
}

export interface GetArticleByIdVariables {
  id: UUIDString;
}

export interface SearchArticlesData {
  articleAnalyses: ({
    article: {
      id: UUIDString;
      title: string;
      date: TimestampString;
      source: string;
      link: string;
      authors: string[];
    } & Article_Key;
      articleId: UUIDString;
      summary?: string | null;
      people?: string[] | null;
      places?: string[] | null;
      agencies?: string[] | null;
      laws?: string[] | null;
      climate?: string[] | null;
      tags?: string[] | null;
  } & ArticleAnalysis_Key)[];
}

export interface SearchArticlesVariables {
  query: string;
}

export interface UpsertArticleData {
  article_upsert: Article_Key;
}

export interface UpsertArticleVariables {
  id: UUIDString;
  title: string;
  date: TimestampString;
  authors?: string[] | null;
  source: string;
  link: string;
}



/* Allow users to create refs without passing in DataConnect */
export function addArticleRef(vars: AddArticleVariables): MutationRef<AddArticleData, AddArticleVariables>;
/* Allow users to pass in custom DataConnect instances */
export function addArticleRef(dc: DataConnect, vars: AddArticleVariables): MutationRef<AddArticleData,AddArticleVariables>;

export function addArticle(vars: AddArticleVariables): MutationPromise<AddArticleData, AddArticleVariables>;
export function addArticle(dc: DataConnect, vars: AddArticleVariables): MutationPromise<AddArticleData,AddArticleVariables>;


/* Allow users to create refs without passing in DataConnect */
export function upsertArticleRef(vars: UpsertArticleVariables): MutationRef<UpsertArticleData, UpsertArticleVariables>;
/* Allow users to pass in custom DataConnect instances */
export function upsertArticleRef(dc: DataConnect, vars: UpsertArticleVariables): MutationRef<UpsertArticleData,UpsertArticleVariables>;

export function upsertArticle(vars: UpsertArticleVariables): MutationPromise<UpsertArticleData, UpsertArticleVariables>;
export function upsertArticle(dc: DataConnect, vars: UpsertArticleVariables): MutationPromise<UpsertArticleData,UpsertArticleVariables>;


/* Allow users to create refs without passing in DataConnect */
export function deleteArticleRef(vars: DeleteArticleVariables): MutationRef<DeleteArticleData, DeleteArticleVariables>;
/* Allow users to pass in custom DataConnect instances */
export function deleteArticleRef(dc: DataConnect, vars: DeleteArticleVariables): MutationRef<DeleteArticleData,DeleteArticleVariables>;

export function deleteArticle(vars: DeleteArticleVariables): MutationPromise<DeleteArticleData, DeleteArticleVariables>;
export function deleteArticle(dc: DataConnect, vars: DeleteArticleVariables): MutationPromise<DeleteArticleData,DeleteArticleVariables>;


/* Allow users to create refs without passing in DataConnect */
export function addArticleAnalysisRef(vars: AddArticleAnalysisVariables): MutationRef<AddArticleAnalysisData, AddArticleAnalysisVariables>;
/* Allow users to pass in custom DataConnect instances */
export function addArticleAnalysisRef(dc: DataConnect, vars: AddArticleAnalysisVariables): MutationRef<AddArticleAnalysisData,AddArticleAnalysisVariables>;

export function addArticleAnalysis(vars: AddArticleAnalysisVariables): MutationPromise<AddArticleAnalysisData, AddArticleAnalysisVariables>;
export function addArticleAnalysis(dc: DataConnect, vars: AddArticleAnalysisVariables): MutationPromise<AddArticleAnalysisData,AddArticleAnalysisVariables>;


/* Allow users to create refs without passing in DataConnect */
export function deleteArticleAnalysisRef(vars?: DeleteArticleAnalysisVariables): MutationRef<DeleteArticleAnalysisData, DeleteArticleAnalysisVariables>;
/* Allow users to pass in custom DataConnect instances */
export function deleteArticleAnalysisRef(dc: DataConnect, vars?: DeleteArticleAnalysisVariables): MutationRef<DeleteArticleAnalysisData,DeleteArticleAnalysisVariables>;

export function deleteArticleAnalysis(vars?: DeleteArticleAnalysisVariables): MutationPromise<DeleteArticleAnalysisData, DeleteArticleAnalysisVariables>;
export function deleteArticleAnalysis(dc: DataConnect, vars?: DeleteArticleAnalysisVariables): MutationPromise<DeleteArticleAnalysisData,DeleteArticleAnalysisVariables>;


/* Allow users to create refs without passing in DataConnect */
export function getArticleByIdRef(vars: GetArticleByIdVariables): QueryRef<GetArticleByIdData, GetArticleByIdVariables>;
/* Allow users to pass in custom DataConnect instances */
export function getArticleByIdRef(dc: DataConnect, vars: GetArticleByIdVariables): QueryRef<GetArticleByIdData,GetArticleByIdVariables>;

export function getArticleById(vars: GetArticleByIdVariables): QueryPromise<GetArticleByIdData, GetArticleByIdVariables>;
export function getArticleById(dc: DataConnect, vars: GetArticleByIdVariables): QueryPromise<GetArticleByIdData,GetArticleByIdVariables>;


/* Allow users to create refs without passing in DataConnect */
export function getArticleAnalysisByIdRef(vars: GetArticleAnalysisByIdVariables): QueryRef<GetArticleAnalysisByIdData, GetArticleAnalysisByIdVariables>;
/* Allow users to pass in custom DataConnect instances */
export function getArticleAnalysisByIdRef(dc: DataConnect, vars: GetArticleAnalysisByIdVariables): QueryRef<GetArticleAnalysisByIdData,GetArticleAnalysisByIdVariables>;

export function getArticleAnalysisById(vars: GetArticleAnalysisByIdVariables): QueryPromise<GetArticleAnalysisByIdData, GetArticleAnalysisByIdVariables>;
export function getArticleAnalysisById(dc: DataConnect, vars: GetArticleAnalysisByIdVariables): QueryPromise<GetArticleAnalysisByIdData,GetArticleAnalysisByIdVariables>;


/* Allow users to create refs without passing in DataConnect */
export function getAllArticlesRef(): QueryRef<GetAllArticlesData, undefined>;/* Allow users to pass in custom DataConnect instances */
export function getAllArticlesRef(dc: DataConnect): QueryRef<GetAllArticlesData,undefined>;

export function getAllArticles(): QueryPromise<GetAllArticlesData, undefined>;
export function getAllArticles(dc: DataConnect): QueryPromise<GetAllArticlesData,undefined>;


/* Allow users to create refs without passing in DataConnect */
export function searchArticlesRef(vars: SearchArticlesVariables): QueryRef<SearchArticlesData, SearchArticlesVariables>;
/* Allow users to pass in custom DataConnect instances */
export function searchArticlesRef(dc: DataConnect, vars: SearchArticlesVariables): QueryRef<SearchArticlesData,SearchArticlesVariables>;

export function searchArticles(vars: SearchArticlesVariables): QueryPromise<SearchArticlesData, SearchArticlesVariables>;
export function searchArticles(dc: DataConnect, vars: SearchArticlesVariables): QueryPromise<SearchArticlesData,SearchArticlesVariables>;


