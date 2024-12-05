"""
A set of functions to interact with the news database
Reads, writes, and searches the db

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE articles (
    id UUID PRIMARY KEY,
    title TEXT NOT NULL,
    date TIMESTAMP NOT NULL,
    authors TEXT[] NOT NULL,
    source TEXT NOT NULL,
    link TEXT NOT NULL
);

CREATE TABLE article_analysis (
    article_id UUID PRIMARY KEY REFERENCES articles(id),
    summary TEXT,
    people TEXT[],
    places TEXT[],
    agencies TEXT[],
    laws TEXT[],
    climate TEXT[],
    tags TEXT[]
);
"""

from typing import Optional, Dict, Any
import uuid
from datetime import datetime
import sqlalchemy
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from data_ingestors.data import NewsData
from google.cloud.sql.connector import Connector
import atexit


# Initialize Connector object
connector = Connector()

# Database configuration - you might want to load these from environment variables
INSTANCE_CONNECTION_NAME = "your-project:your-region:your-instance"
DB_USER = "your-db-user"
DB_PASS = "your-db-password"
DB_NAME = "news"

def get_engine() -> Engine:
    """Create database connection engine using Cloud SQL Python Connector"""
    def getconn():
        return connector.connect(
            INSTANCE_CONNECTION_NAME,
            "pg8000",
            user=DB_USER,
            password=DB_PASS,
            db=DB_NAME,
        )
    
    engine = create_engine(
        "postgresql+pg8000://",
        creator=getconn,
    )
    return engine

def _format_article_for_db(news: NewsData) -> Dict[str, Any]:
    """Format article data for the Articles table"""
    return {
        "id": str(uuid.uuid4()),  # Generate new UUID for the article
        "title": news.title,
        "date": news.date,
        "authors": news.authors,  # PostgreSQL array type
        "source": news.source,
        "link": news.link,
    }

def _format_analysis_for_db(article_id: str, news: NewsData) -> Dict[str, Any]:
    """Format analysis data for the ArticleAnalysis table"""
    return {
        "article_id": article_id,
        "summary": news.summary,
        "people": [],  # These fields would need to be populated by your analysis logic
        "places": [],
        "agencies": [],
        "laws": [],
        "climate": [],
        "tags": [],
    }

def _filter_existing_articles(engine: Engine, links: list[str]) -> list[str]:
    """Filter out articles that already exist in the database based on their links"""
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT link FROM articles WHERE link = ANY(:links)"),
            {"links": links}
        )
        existing_links = {row[0] for row in result}
    
    return [link for link in links if link not in existing_links]

def insert_news(engine: Engine, news_items: list[NewsData]) -> None:
    """
    Insert news into the database (both Articles and ArticleAnalysis tables)
    :param engine: The database engine
    :param news_items: A list of NewsData objects
    """
    # Filter out existing articles
    links = [news.link for news in news_items]
    new_links = _filter_existing_articles(engine, links)
    new_news = [news for news in news_items if news.link in new_links]
    
    if not new_news:
        return

    with engine.connect() as conn:
        # Insert articles and collect their IDs
        for news in new_news:
            article_data = _format_article_for_db(news)
            
            # Insert article
            conn.execute(
                text("""
                    INSERT INTO articles (id, title, date, authors, source, link)
                    VALUES (:id, :title, :date, :authors, :source, :link)
                """),
                article_data
            )
            
            # Insert article analysis
            analysis_data = _format_analysis_for_db(article_data["id"], news)
            conn.execute(
                text("""
                    INSERT INTO article_analysis 
                    (article_id, summary, people, places, agencies, laws, climate, tags)
                    VALUES 
                    (:article_id, :summary, :people, :places, :agencies, :laws, :climate, :tags)
                """),
                analysis_data
            )
        
        conn.commit()

def search_articles(engine: Engine, query: str) -> list[Dict[str, Any]]:
    """
    Search articles and their analysis
    :param engine: The database engine
    :param query: The query to search for
    :return: A list of article dictionaries with their analysis
    """
    clean_query = f"%{query.strip().lower()}%"
    
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT 
                    a.*,
                    aa.summary,
                    aa.people,
                    aa.places,
                    aa.agencies,
                    aa.laws,
                    aa.climate,
                    aa.tags
                FROM articles a
                LEFT JOIN article_analysis aa ON a.id = aa.article_id
                WHERE 
                    LOWER(a.title) LIKE :query 
                    OR :query = ANY(aa.tags)
                ORDER BY a.date DESC
            """),
            {"query": clean_query}
        )
        
        return [dict(row) for row in result]

def get_article_by_id(engine: Engine, article_id: str) -> Optional[Dict[str, Any]]:
    """
    Get article and its analysis by ID
    :param engine: The database engine
    :param article_id: The article ID to search for
    :return: Article dictionary with its analysis
    """
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT 
                    a.*,
                    aa.summary,
                    aa.people,
                    aa.places,
                    aa.agencies,
                    aa.laws,
                    aa.climate,
                    aa.tags
                FROM articles a
                LEFT JOIN article_analysis aa ON a.id = aa.article_id
                WHERE a.id = :id
            """),
            {"id": article_id}
        )
        row = result.fetchone()
        
        return dict(row) if row else None

def get_all_articles(engine: Engine, limit: int = 100) -> list[Dict[str, Any]]:
    """
    Get all articles with their analysis
    :param engine: The database engine
    :param limit: Maximum number of articles to return
    :return: List of article dictionaries with their analysis
    """
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT 
                    a.*,
                    aa.summary,
                    aa.people,
                    aa.places,
                    aa.agencies,
                    aa.laws,
                    aa.climate,
                    aa.tags
                FROM articles a
                LEFT JOIN article_analysis aa ON a.id = aa.article_id
                ORDER BY a.date DESC
                LIMIT :limit
            """),
            {"limit": limit}
        )
        
        return [dict(row) for row in result]

# Clean up connector on program exit
atexit.register(connector.close)

if __name__ == "__main__":
    engine = get_engine()
    articles = get_all_articles(engine)
    print(f"Found {len(articles)} articles")