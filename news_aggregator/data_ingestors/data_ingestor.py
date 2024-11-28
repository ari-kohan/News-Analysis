"""
The base class for ingesting data from a source.
"""

import abc
from typing import List
from enum import Enum, auto


class IngestorType(Enum):
    RSS = auto()
    API = auto()


class DataIngestor(abc.ABC):
    """
    An abstract class to handle the reading and formatting of rss feed data
    """
    url: str
    type: IngestorType

    @abc.abstractmethod
    def clean_data(self, data: List[dict]) -> List[dict]:
        """
        Clean the data to remove any html tags.
        :param data: The data to clean
        :return: The cleaned data
        """
        raise NotImplementedError

    @abc.abstractmethod
    def format_data(self, data: List[dict]) -> List[dict]:
        """
        Format the data to a standard format.
        :param data: The data to format
        :return: The formatted data
        """
        raise NotImplementedError
