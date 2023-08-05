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


class GesetzeImInternet(Scraper):
    """
    Utilities for scraping 'gesetze-im-internet.de'
    """

    # Individual identifier
    identifier: str = "gesetze"

    def scrape(self, output_file: str, wait: int = 2) -> None:
        """
        Scrapes 'gesetze-im-internet.de' for legal norms

        :param output_file: str Path to merged data file
        :param wait: int Time to wait before scraping next law
        :return: None
        """

        # Create list of data files
        data_files = []

        # Iterate over relevant charset
        for char in "ABCDEFGHIJKLMNOPQRSTUVWYZ123456789":
            # Fetch overview page for category letter
            html = self.get_html(
                f"https://www.gesetze-im-internet.de/Teilliste_{char}.html"
            )

            # Parse their HTML & iterate over `p` tags ..
            for link in soup(html).select("#paddingLR12")[0].select("p"):
                # .. extracting data for each law
                law = link.a.text[1:-1]

                # Define data file for current law
                data_file = self.get_file_path(law, "json")

                # If it already exists ..
                if exists(data_file):
                    # (1) .. update list of data files
                    data_files.append(data_file)

                    # (2) .. skip law
                    continue

                slug = link.a["href"][2:-11]
                title = link.a.abbr["title"]

                # .. collecting its information
                node = {
                    "law": law,
                    "slug": slug,
                    "title": title,
                    "headings": {},
                }

                # Fetch index page for each law
                law_html = self.get_html(
                    f"https://www.gesetze-im-internet.de/{slug}/index.html"
                )

                # Iterate over `a` tags ..
                for heading in soup(law_html).select("#paddingLR12")[0].select("td"):
                    # (1) .. skipping headings without `a` tag child
                    if not heading.a:
                        continue

                    # (2) .. skipping headings without `href` attribute in `a` tag child
                    if not heading.a.get("href"):
                        continue

                    # If section identifier available ..
                    if match := re.match(
                        r"(?:§+|Art|Artikel)\.?\s*(\d+(?:\w\b)?)",
                        heading.text,
                        re.IGNORECASE,
                    ):
                        # .. store identifier as key and heading as value
                        node["headings"][match.group(1)] = heading.text.strip()

                    # .. otherwise ..
                    else:
                        # .. store heading as both key and value
                        node["headings"][heading.text.strip()] = heading.text.strip()

                # Store data record
                # (1) Write data to JSON file
                dump_json(node, data_file)

                # (2) Update list of data files
                data_files.append(data_file)

                # Wait for it ..
                time.sleep(wait)

        # Merge data files
        self.build(data_files, output_file)
