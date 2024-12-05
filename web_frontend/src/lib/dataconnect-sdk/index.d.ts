import { ConnectorConfig, DataConnect, QueryRef, QueryPromise, MutationRef, MutationPromise } from 'firebase/data-connect';
export const connectorConfig: ConnectorConfig;

export type TimestampString = string;

export type UUIDString = string;

export type Int64String = string;

export type DateString = string;



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

export interface DeleteArticleData {
  article_delete?: Article_Key | null;
}

export interface DeleteArticleVariables {
  id: UUIDString;
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
      climate?: boolean | null;
    };
  };
}

export interface GetArticleByIdVariables {
  id: UUIDString;
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
export function getArticleByIdRef(vars: GetArticleByIdVariables): QueryRef<GetArticleByIdData, GetArticleByIdVariables>;
/* Allow users to pass in custom DataConnect instances */
export function getArticleByIdRef(dc: DataConnect, vars: GetArticleByIdVariables): QueryRef<GetArticleByIdData,GetArticleByIdVariables>;

export function getArticleById(vars: GetArticleByIdVariables): QueryPromise<GetArticleByIdData, GetArticleByIdVariables>;
export function getArticleById(dc: DataConnect, vars: GetArticleByIdVariables): QueryPromise<GetArticleByIdData,GetArticleByIdVariables>;


