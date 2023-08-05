"""
This module is part of the 'py-gesetze' package,
which is released under GPL-3.0-only license.
"""

import json
import os
from typing import Union


def load_json(json_file: str) -> dict:
    """
    Loads data from JSON file

    :param json_file: str Path to JSON file

    :return: dict Loaded JSON data
    :raises: Exception Error decoding JSON
    """

    try:
        with open(json_file, encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError:
        return {}


def dump_json(data: Union[dict, list], json_file: str) -> None:
    """
    Dumps data to JSON file

    :param data: dict | list Data to be dumped
    :param json_file: str Path to JSON file

    :return: None
    """

    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)


def create_path(path: str) -> None:
    """
    Creates path recursively

    :param path: str Path to directory / file

    :return: None
    """

    # If path does not exist ..
    if not os.path.exists(path):
        # .. attempt to ..
        try:
            # .. create it
            os.makedirs(path)

        # Guard against race condition
        except OSError:
            pass
