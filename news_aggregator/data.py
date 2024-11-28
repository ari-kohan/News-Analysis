from dataclasses import dataclass
from datetime import datetime


@dataclass
class NewsData:
    """
    A class to handle data from a variety of news sources
    """

    uid: str
    # A unique id from the hashed linke
    title: str
    # The title of the news article
    content: str
    # The content of the news article
    date: datetime
    # The date of the news article
    authors: list[str]
    # The authors of the news article
    source: str
    # The source of the news article
    link: str
    # The link to the news article
    summary: str
    # The summary of the news article
