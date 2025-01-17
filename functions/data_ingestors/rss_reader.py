"""
A set of functions to pull news from various api sources
"""

from typing import List, Optional
import json
import feedparser
import abc
import re
import uuid
from datetime import datetime
import zoneinfo
from logging import log
import bs4
from time import mktime

from .data import NewsData
from .data_ingestor import DataIngestor, IngestorType


class RSSReader(DataIngestor):
    """A base class for RSS based data ingestors"""

    date_format: str

    type = IngestorType.RSS

    def fetch(
        self,
        last_fetched_time: Optional[datetime] = None,
        last_etag: Optional[str] = None,
    ):
        """
        Fetch the most recent RSS feed
        Fetch logic credit to https://brntn.me/blog/respectfully-requesting-rss-feeds/
        """

        headers = {
            "User-Agent": "TrumpTracker"  # (+https://brntn.me/blog/respectfully-requesting-rss-feeds/)"
        }

        response = feedparser.parse(
            self.url,
            request_headers=headers,
            etag=last_etag,
            modified=last_fetched_time,
        )

        # return immediately if 304 is returned
        if response.status == 304:
            # content is unchanged
            log(f"[fetch] {self.url} is unchanged")
            self.last_checked_utc = datetime.now(tz=zoneinfo.ZoneInfo("UTC"))
            return

        # backoff if we receive a 429 response
        if response.status != 200:
            log.info(f"[fetch] {self.url} returned {response.status}")
            return

        # save ETag and last checked timestamp
        etag = None
        if response.headers.get("etag"):
            etag = response.headers["etag"]

        return response, etag


class TheHillRSSReader(RSSReader):
    url: str = "https://thehill.com/homenews/feed/"

    def clean_data(self, data: List[feedparser.FeedParserDict]) -> List[dict]:
        """
        Clean the data to remove any html tags.
        :param data: The data to clean
        :return: The cleaned data
        TODO clean with beautifulsoup
        """
        for entry in data.entries:
            entry["content"][0]["value"] = bs4.BeautifulSoup(
                entry["content"][0]["value"], "html.parser"
            ).text
            entry["content"][0]["value"] = entry["content"][0]["value"].replace(
                "\n\t\t\n\t\t\n\n\n", ""
            )
            # strip all newlines and tabs
            entry["content"][0]["value"] = entry["content"][0]["value"].replace(
                "\n", " "
            )
            entry["content"][0]["value"] = entry["content"][0]["value"].replace(
                "\t", " "
            )
        return data

    def format_data(self, data: List[feedparser.FeedParserDict]) -> List[dict]:
        """
        Format the data to a standard format.
        :param data: The data to format
        :return: The formatted data
        """
        articles = []
        for entry in data.entries:
            articles.append(
                {
                    "title": entry["title"],
                    "link": entry["link"],
                    "authors": [author["name"] for author in entry["authors"]],
                    "date": datetime.fromtimestamp(mktime(entry["updated_parsed"])),
                    "content": entry["content"][0]["value"],
                    "source": self.url,
                    "uid": str(uuid.uuid3(uuid.NAMESPACE_URL, entry["link"])),
                }
            )
        return articles


class ProPublicaRSSReader(RSSReader):
    url: str = "https://www.propublica.org/feeds/propublica/main"

    def clean_data(self, data: List[feedparser.FeedParserDict]) -> List[dict]:
        """
        Clean the data to remove any html tags.
        :param data: The data to clean
        :return: The cleaned data
        TODO clean with beautifulsoup
        """
        for entry in data.entries:
            entry["summary"] = bs4.BeautifulSoup(entry["summary"], "html.parser").text
            entry["summary"] = entry["summary"].replace("\n", " ")
            entry["summary"] = entry["summary"].replace("\t", " ")
        return data

    def format_data(self, data: List[feedparser.FeedParserDict]) -> List[dict]:
        """
        Format the data to a standard format.
        :param data: The data to format
        :return: The formatted data
        """
        articles = []
        for entry in data.entries:
            articles.append(
                {
                    "title": entry["title"],
                    "link": entry["link"],
                    "authors": entry["author"],
                    "date": datetime.fromtimestamp(mktime(entry["updated_parsed"])),
                    "content": entry["summary"],
                    "source": self.url,
                    "uid": str(uuid.uuid3(uuid.NAMESPACE_URL, entry["link"])),
                }
            )
        return articles


def save_rss_file(filepath: str, data: dict) -> None:
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def read_rss_feeds() -> None:
    """
    Read the rss feeds from the rss_sources list.
    """
    i = 0
    for source in RSSReader.__subclasses__():
        s = source()
        data = s.fetch()
        data = s.clean_data(data)
        data = s.format_data(data)
        news_data = [
            NewsData(
                title=item["title"],
                link=item["link"],
                authors=item["authors"],
                date=item["date"],
                summary=item["summary"],
                content=item["content"],
                source=item["source"],
                uid=item["uid"],
            )
            for item in data
        ]
        # save_rss(f"rss_feed_{i}.json", data)
        i += 1
    return news_data


if __name__ == "__main__":
    # read_rss_feeds()
    reader = ProPublicaRSSReader()
    data, _ = reader.fetch()
    data = reader.clean_data(data)
    breakpoint()
    data = reader.format_data(data)
    breakpoint()
    # save_rss_file("rss_feed.json", data)
