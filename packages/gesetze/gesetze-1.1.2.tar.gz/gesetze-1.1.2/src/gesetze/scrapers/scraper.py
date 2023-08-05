"""
This module is part of the 'py-gesetze' package,
which is released under GPL-3.0-only license.
"""

from abc import ABC, abstractmethod
import hashlib
from os import getcwd
from os.path import exists
from shutil import rmtree
from typing import Optional

from bs4 import BeautifulSoup
from requests import get

from ..utils import create_path, dump_json, load_json


class Scraper(ABC):
    """
    Utilities for scraping providers
    """

    # Individual identifier
    identifier: Optional[str] = None

    def __init__(self, path: str) -> None:
        """
        Initializes download directory

        :param path: str Path to directory
        :return: None
        """

        # Create data directory
        # (1) Define its path
        self.dir = f"{path}/.{self.identifier}"

        # (2) Create (if necessary)
        create_path(self.dir)

    def get_html(self, url: str) -> str:
        """
        Fetches HTML of given URL

        :param url: str Target URL
        :return: str Target HTML
        """

        # Determine path to HTML file
        file = self.get_file_path(url, "html")

        if not exists(file):
            html = get(url, timeout=10).text

            with open(file, "w", encoding="utf-8") as html_file:
                html_file.write(html)

        else:
            with open(file, encoding="utf-8") as html_file:
                html = html_file.read()

        return html

    def get_file_path(self, law: str, ext: str) -> str:
        """
        Determines path to JSON data file

        :param law: str Law title
        :param law: str File extension
        :return: str Path to data file
        """

        # Use hashed law title as filename
        filename = hashlib.md5(law.encode("utf-8"), usedforsecurity=False).hexdigest()

        # Build its path
        return f"{self.dir}/{filename}.{ext}"

    def build(self, data_files: list, output_file: Optional[str] = None) -> None:
        """
        Merges JSON files & removes them afterwards

        :param data_files: list List of data files
        :param output_file: str Path to merged data file
        :return: None
        """

        # Create data buffer
        data = {}

        # Iterate over data files
        for data_file in data_files:
            # Load data & update data buffer
            node = load_json(data_file)
            data[node["law"].lower()] = node

        # if target file not specified ..
        if output_file is None:
            # .. use current working directory & identifier as fallback
            output_file = f"{getcwd()}/{self.identifier}.json"

        # Write complete dataset to JSON file
        dump_json(data, output_file)

        # Remove temporary files
        rmtree(self.dir)

    @abstractmethod
    def scrape(self, output_file: str, wait: int = 2) -> None:
        """
        Scrapes website for legal norms

        :param output_file: str Path to merged data file
        :param wait: int Time to wait before scraping next law
        :return: None
        """


def soup(html: str) -> BeautifulSoup:
    """
    Converts HTML to 'BeautifulSoup' object

    :param html: str Target HTML

    :return: bs4.BeautifulSoup 'BeautifulSoup' object
    """

    return BeautifulSoup(html, "lxml")
