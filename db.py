"""
A set of functions to interact with the news database
Reads, writes, and searches the db
"""
from typing import Optional
import sqlite3
from data import NewsData

# conn = sqlite3.connect("news.db")
# cursor = conn.cursor()

# cursor.execute(
#     """CREATE TABLE IF NOT EXISTS news (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     uid TEXT,
#     title TEXT,
#     content TEXT,
#     date DATETIME,
#     authors TEXT,
#     source TEXT,
#     link TEXT,
#     summary TEXT
# )"""
# )

# conn.commit()
# conn.close()


def format_news_for_db(news: list[NewsData]) -> list[tuple]:
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
            item.date.strftime('%Y-%m-%d %H:%M:%S'),
            ", ".join(item.authors),  # TODO make a list again
            item.source,
            item.link,
            item.summary,
        )
        for item in news
    ]


def insert_news(news: list[NewsData]) -> None:
    """
    Insert news into the database
    :param news: A list of NewsData objects
    """
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()
    formatted_news = format_news_for_db(news)
    cursor.executemany(
        """INSERT INTO news (uid, title, content, date, authors, source, link, summary) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        formatted_news,
    )
    conn.commit()
    conn.close()


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


def search_news(query: str) -> list[NewsData]:
    """
    Search the database for news
    :param query: The query to search for
    :return: A list of NewsData objects
    # TODO maybe use full text search?
    """
    clean_query = _clean_query(query)
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM news WHERE title LIKE ? OR content LIKE ? OR authors LIKE ? OR source LIKE ? OR summary LIKE ? ORDER BY date DESC",
        (clean_query, clean_query, clean_query, clean_query, clean_query),
    )
    news = cursor.fetchall()
    print(news)
    conn.close()
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


def get_news_by_uid(uid: str) -> Optional[NewsData]:
    """
    Get news by uid
    :param uid: The uid to search for
    :return: A NewsData object
    """
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM news WHERE uid = ?", (uid,))
    news = cursor.fetchone()
    conn.close()
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


def get_all_news() -> list[NewsData]:
    """
    Get all news
    :return: A list of NewsData objects
    """
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM news ORDER BY date DESC")
    news = cursor.fetchall()
    conn.close()
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
    #print(news[0])
    uid = "d26099cd-4a07-35d3-8ca7-d2078fda61fc"
    article = get_news_by_uid(uid)
    print(article)
    search = search_news("Trump")
    #print(search)
