"""
This module is part of the 'py-gesetze' package,
which is released under GPL-3.0-only license.
"""

from abc import ABC, abstractmethod
from os.path import dirname, exists, realpath
from typing import Optional

from ..helpers import analyze
from ..utils import load_json


class Driver(ABC):
    """
    Utilities for dealing with providers
    """

    # Individual identifier
    identifier: Optional[str] = None

    def __init__(self, file: Optional[str] = None) -> None:
        """
        Creates 'Driver' instance

        :param file: str Path to (custom) data file

        :raises: Exception Invalid law
        """

        # Set default index file
        if file is None:
            file = f"{dirname(__file__)}/../data/{self.identifier}.json"

        # Fail early if file does not exist
        if not exists(file):
            raise Exception(f'File does not exist: "{realpath(file)}"')

        # Load law library data
        self.library = load_json(file)

    def validate(self, string: str) -> bool:
        """
        Validates a single legal norm (current provider)

        :param string: str Legal norm
        :return: bool Whether legal norm is valid (= linkable)
        """

        # Fail early when string is empty
        if not string:
            return False

        # Analyze legal norm
        data = analyze(string)

        # Attempt to ..
        try:
            # (1) .. get lowercase identifier for current law
            identifier = data["gesetz"].lower()

            # (2) .. check whether current law contains norm
            return data["norm"] in self.library[identifier]["headings"]

        except KeyError:
            return False

    def build_title(self, data: dict, mode: str) -> str:
        """
        Builds description for corresponding legal norm (used as `title` attribute)

        :param data: dict Legal data
        :param mode: str Output mode, either 'light', 'normal' or 'full' (default: False)
        :return: str Title attribute
        :raises: Exception Invalid law
        """

        # Get lowercase identifier for current law
        identifier = data["gesetz"].lower()

        # Fail early if law is unavailable
        if identifier not in self.library:
            raise Exception(f'Invalid law: "{data["gesetz"]}"')

        # Get data about current law
        law = self.library[identifier]

        # Determine `title` attribute
        if mode == "light":
            return law["law"]

        if mode == "normal":
            return law["title"]

        if mode == "full":
            return law["headings"][data["norm"]]

        return ""

    @abstractmethod
    def build_url(self, data: dict) -> str:
        """
        Builds URL for corresponding legal norm (used as `href` attribute)

        :param data: dict Legal data
        :return: str Target URL
        """
