from dataclasses import dataclass
from datetime import datetime


@dataclass
class NewsAnalysis:
    """
    A class to store analysis of news articles
    """

    uid: str
    # The ID of the analyzed article
    summary: str
    # Summary of the article content
    people: list[str]
    # People mentioned in the article
    places: list[str]
    # Places mentioned in the article
    agencies: list[str]
    # Government agencies mentioned
    laws: list[str]
    # Laws or regulations mentioned
    climate: list[str]
    # Climate-related terms mentioned
    tags: list[str]
    # General topic tags


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
    analysis: NewsAnalysis
    # The additional analysis of this news article
