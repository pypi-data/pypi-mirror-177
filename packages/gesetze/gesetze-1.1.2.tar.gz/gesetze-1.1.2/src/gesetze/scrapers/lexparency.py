"""
This module is part of the 'py-gesetze' package,
which is released under GPL-3.0-only license.
"""

# pylint: disable=R0801

from os.path import exists
import re
import time

from ..utils import dump_json
from .scraper import Scraper, soup


class Lexparency(Scraper):
    """
    Utilities for scraping 'lexparency.de'
    """

    # Individual identifier
    identifier: str = "lexparency"

    def scrape(self, output_file: str, wait: int = 2) -> None:
        """
        Scrapes 'lexparency.de' for legal norms

        :param output_file: str Path to merged data file
        :param wait: int Time to wait before scraping next law
        :return: None
        """

        # Fetch overview page
        html = self.get_html("https://lexparency.de")

        # Create list of data files
        data_files = []

        # Parse their HTML & iterate over `a` tags ..
        for link in soup(html).select("#featured-acts")[0].select("a"):
            # .. extracting data for each law
            law = link.text.strip()

            # If abbreviation available ..
            if law_match := re.match(r".*\((.*)\)$", law):
                # .. store it as shorthand for current law
                law = law_match.group(1)

            # Define data file for current law
            data_file = self.get_file_path(law, "json")

            # If it already exists ..
            if exists(data_file):
                # (1) .. update list of data files
                data_files.append(data_file)

                # (2) .. skip law
                continue

            slug = link["href"][4:]

            # .. collecting its information
            node = {
                "law": law,
                "slug": slug,
                "title": "",
                "headings": {},
            }

            # Fetch index page for each law
            law_html = self.get_html(f"https://lexparency.de/eu/{slug}")

            # Get title
            node["title"] = get_title(law_html)

            # Iterate over `li` tags ..
            for heading in (
                soup(law_html)
                .select("#toccordion")[0]
                .find_all("li", attrs={"class": "toc-leaf"})
            ):
                # (1) .. skipping headings without `a` tag child
                if not heading.a:
                    continue

                # (2) .. skipping headings without `href` attribute in `a` tag child
                if not heading.a.get("href"):
                    continue

                string = heading.text.replace("—", "-")

                # If section identifier available ..
                if match := re.match(
                    r"(?:§+|Art|Artikel)\.?\s*(\d+(?:\w\b)?)", string, re.IGNORECASE
                ):
                    # .. store identifier as key and heading as value
                    node["headings"][match.group(1)] = string.replace("§  ", "§ ")

                # .. otherwise ..
                else:
                    # .. store heading as both key and value
                    node["headings"][string] = string

            # Store data record
            # (1) Write data to JSON file
            dump_json(node, data_file)

            # (2) Update list of data files
            data_files.append(data_file)

            # Wait for it ..
            time.sleep(wait)

        # Merge data files
        self.build(data_files, output_file)


def get_title(html: str) -> str:
    """
    Creates law title from HTML contents

    :param html: str HTML contents
    :return: str Law title
    """

    # Determine title
    # (1) Create empty list
    title = []

    # (2) Convert first character of second entry (= 'title essence') to lowercase
    for i, string in enumerate(list(soup(html).select("h1")[0].stripped_strings)):
        if i == 1:
            string = string[:1].lower() + string[1:]

        title.append(string)

    # (3) Create title from strings
    return " ".join(title).strip()
