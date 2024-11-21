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

from data import NewsData
from data_ingestor import DataIngestor

RSS_SOURCES = ["https://thehill.com/homenews/feed/"]
DATE_FORMAT = "%a, %d %b %Y %H:%M:%S %z"  # "Tue, 19 Nov 2024 22:29:18 +0000"

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


class RSSReader(DataIngestor):
    """A base class for RSS based data ingestors"""

    last_fetched_time: Optional[datetime] = None
    last_etag: Optional[str] = None
    fetch_interval: int = 3600

    def fetch(self):
        """
        Fetch the most recent RSS feed
        Fetch logic credit to https://brntn.me/blog/respectfully-requesting-rss-feeds/
        """
        # do not fetch if we are within fetch interval
        # if (
        #     self.last_fetched_time
        #     and (
        #         datetime.now(tz=zoneinfo.ZoneInfo("UTC")) - self.last_fetched_time
        #     ).seconds
        #     < self.fetch_interval
        # ):
        #     log.info(
        #         f"[fetch] {self.url} was checked less than {self.fetch_interval} seconds ago"
        #     )
        #     return

        headers = {
            "User-Agent": "TrumpTracker"  # (+https://brntn.me/blog/respectfully-requesting-rss-feeds/)"
        }

        response = feedparser.parse(
            self.url,
            request_headers=headers,
            etag=self.last_etag,
            modified=self.last_fetched_time,
        )

        # return immediately if 304 is returned
        if response.status == 304:
            # content is unchanged
            log.info(f"[fetch] {self.url} is unchanged")
            self.last_checked_utc = datetime.now(tz=zoneinfo.ZoneInfo("UTC"))
            return

        # backoff if we receive a 429 response
        if response.status != 200:
            log.info(f"[fetch] {self.url} returned {response.status}")
            self.check_interval = self.check_interval + self.check_interval
            if self.check_interval > 60 * 60 * 24:
                self.check_interval = 60 * 60 * 24
            self.last_checked_utc = datetime.now(tz=zoneinfo.ZoneInfo("UTC"))
            self.save()
            return

        # save ETag and last checked timestamp
        if response.headers.get("etag"):
            self.last_etag = response.headers["etag"]

        self.last_fetched_time = datetime.now(tz=zoneinfo.ZoneInfo("UTC"))
        return response


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
            entry["summary"] = bs4.BeautifulSoup(entry["summary"], "html.parser").text
            # strip all html tags and markup
            # strip style tags and their content
            # entry["content"][0]["value"] = re.sub(
            #     r"<style[^>]*>.*?</style>",
            #     "",
            #     entry["content"][0]["value"],
            #     flags=re.DOTALL,
            # )
            # entry["content"][0]["value"] = re.sub(
            #     r"<[^>]*>", "", entry["content"][0]["value"]
            # )
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
                    "date": datetime.strptime(entry["published"], DATE_FORMAT),
                    "summary": entry["summary"],
                    "content": entry["content"][0]["value"],
                    "source": self.url,
                    "uid": str(uuid.uuid3(uuid.NAMESPACE_URL, entry["link"])),
                }
            )
        return articles


def get_rss(url: str) -> dict:
    return feedparser.parse(url)


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
    read_rss_feeds()
    # reader = TheHillRSSReader()
    # reader.fetch()
