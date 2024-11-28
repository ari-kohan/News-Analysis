"""
A set of functions to interact with the news database
Reads, writes, and searches the db
"""

from typing import Optional
import sqlite3
from data import NewsData

DATABASE = "news.db"


def _format_news_for_db(news: list[NewsData]) -> list[tuple]:
    """
    Format news for the database
    :param news: A list of NewsData objects
    :return: A list of tuples
    """
    return [
        (
            item.uid,
            item.title,
            item.content,
            item.date.strftime("%Y-%m-%d %H:%M:%S"),
            ", ".join(item.authors),  # TODO make a list again
            item.source,
            item.link,
            item.summary,
        )
        for item in news
    ]


def _filter_existing_news(
    cursor: sqlite3.Cursor, news: list[NewsData]
) -> list[NewsData]:
    """
    Filter out news that already exists in the database
    :param cursor: The database cursor
    :param news: A list of NewsData objects
    :return: A list of NewsData objects
    """
    existing_news = cursor.execute("SELECT uid FROM news").fetchall()
    existing_uids = [uid[0] for uid in existing_news]
    return [news for news in news if news.uid not in existing_uids]


def insert_news(db_connection: sqlite3.Connection, news: list[NewsData]) -> None:
    """
    Insert news into the database
    :param db_connection: The database connection
    :param news: A list of NewsData objects
    """
    cursor = db_connection.cursor()

    formatted_news = _filter_existing_news(cursor, news)
    formatted_news = _format_news_for_db(formatted_news)
    cursor.executemany(
        """INSERT INTO news (uid, title, content, date, authors, source, link, summary) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        formatted_news,
    )
    db_connection.commit()


def _clean_query(query: str) -> str:
    """
    :return: a cleaned query
    """
    # Escape single quotes
    query = query.replace("'", "''")

    # Prevent SQL injection
    query = query.replace(";", "")
    query = query.replace("--", "")
    query = query.replace("+", " ")
    query = query.strip()
    query = query.lower()
    query = f"%{query}%"

    return query


def search_news(db_connection: sqlite3.Connection, query: str) -> list[NewsData]:
    """
    Search the database for news
    :param db_connection: The database connection
    :param query: The query to search for
    :return: A list of NewsData objects
    # TODO maybe use full text search?
    """
    clean_query = _clean_query(query)
    cursor = db_connection.cursor()
    cursor.execute(
        "SELECT * FROM news WHERE title LIKE ? OR content LIKE ? OR authors LIKE ? OR source LIKE ? OR summary LIKE ? ORDER BY date DESC",
        (clean_query, clean_query, clean_query, clean_query, clean_query),
    )
    news = cursor.fetchall()
    return [
        NewsData(
            uid=item[1],
            title=item[2],
            content=item[3],
            date=item[4],
            authors=item[5],
            source=item[6],
            link=item[7],
            summary=item[8],
        )
        for item in news
    ]


def get_news_by_uid(db_connection: sqlite3.Connection, uid: str) -> Optional[NewsData]:
    """
    Get news by uid
    :param db_connection: The database connection
    :param uid: The uid to search for
    :return: A NewsData object
    """
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM news WHERE uid = ?", (uid,))
    news = cursor.fetchone()
    if not news:
        return None
    return NewsData(
        uid=news[1],
        title=news[2],
        content=news[3],
        date=news[4],
        authors=news[5],
        source=news[6],
        link=news[7],
        summary=news[8],
    )


def get_all_news(db_connection: sqlite3.Connection) -> list[NewsData]:
    """
    Get all news
    :param db_connection: The database connection
    :return: A list of NewsData objects
    """
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM news ORDER BY date DESC")
    news = cursor.fetchall()
    return [
        NewsData(
            uid=item[1],
            title=item[2],
            content=item[3],
            date=item[4],
            authors=item[5],
            source=item[6],
            link=item[7],
            summary=item[8],
        )
        for item in news
    ]


if __name__ == "__main__":
    news = get_all_news()
    # print(news[0])
    uid = "d26099cd-4a07-35d3-8ca7-d2078fda61fc"
    article = get_news_by_uid(uid)
    print(article)
    search = search_news("Trump")
    # print(search)
