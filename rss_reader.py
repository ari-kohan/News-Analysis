"""
A set of functions to pull news from various api sources
"""
import json
import feedparser
import abc
import re
import uuid
RSS_SOURCES = ["https://thehill.com/homenews/feed/"]

"""
Data Format
{
    "title": str,
    "link": str,
    "authors": list[str],
    "date": str,
    "summary": str,
    "content": str,
    "source": str,
    "uid": str
}
"""


class RSSReader(abc.ABC):
    url: str

    @abc.abstractmethod
    def clean_data(self, data: dict) -> dict:
        """
        Clean the data to remove any html tags.
        """
        raise NotImplementedError
    
    @abc.abstractmethod
    def format_data(self, data: dict) -> dict:
        """
        Format the data to a standard format.
        """
        raise NotImplementedError


class TheHillRSSReader(RSSReader):
    url: str = "https://thehill.com/homenews/feed/"

    def clean_data(self, data: dict) -> dict:
        """
        Clean the data to remove any html tags.
        """
        for entry in data.entries:
            entry['summary'] = re.sub(r'<[^>]*>', '', entry['summary'])
            # strip all html tags and markup
            # strip style tags and their content
            entry['content'][0]['value'] = re.sub(r'<style[^>]*>.*?</style>', '', entry['content'][0]['value'], flags=re.DOTALL)
            entry['content'][0]['value'] = re.sub(r'<[^>]*>', '', entry['content'][0]['value'])
            entry['content'][0]['value'] = entry['content'][0]['value'].replace('\n\t\t\n\t\t\n\n\n', '')
            # strip all newlines and tabs
            entry['content'][0]['value'] = entry['content'][0]['value'].replace('\n', ' ')
            entry['content'][0]['value'] = entry['content'][0]['value'].replace('\t', ' ')
        return data
    
    def format_data(self, data: dict) -> dict:
        """
        Format the data to a standard format.
        """
        articles = []
        for entry in data.entries:
            articles.append({
                "title": entry['title'],
                "link": entry['link'],
                "authors": [author['name'] for author in entry['authors']],
                "date": entry['published'],
                "summary": entry['summary'],
                "content": entry['content'][0]['value'],
                "source": self.url,
                "uid": str(uuid.uuid3(uuid.NAMESPACE_URL, entry['link']))
            })
        return articles


def get_rss(url: str) -> dict:
    return feedparser.parse(url)

def save_rss(filepath: str, data: dict) -> None:
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def read_rss_feeds() -> None:
    """
    Read the rss feeds from the rss_sources list.
    """
    i = 0
    for source in RSSReader.__subclasses__():
        s = source()
        data = feedparser.parse(s.url)
        data = s.clean_data(data)
        data = s.format_data(data)
        save_rss(f"rss_feed_{i}.json", data)
        i += 1


if __name__ == "__main__":
    read_rss_feeds()

