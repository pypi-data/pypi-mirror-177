"""
This module is part of the 'py-gesetze' package,
which is released under GPL-3.0-only license.
"""

# pylint: disable=R0801

from .driver import Driver


class GesetzeImInternet(Driver):
    """
    Utilities for dealing with 'gesetze-im-internet.de'
    """

    # Individual identifier
    identifier: str = "gesetze"

    def build_url(self, data: dict) -> str:
        """
        Builds URL for corresponding legal norm (used as `href` attribute)

        :param data: dict Legal data
        :return: str Target URL
        :raises: Exception Invalid law
        """

        # Get lowercase identifier for current law
        identifier = data["gesetz"].lower()

        # Fail early if law is unavailable
        if identifier not in self.library:
            raise Exception(f'Invalid law: "{data["gesetz"]}"')

        # Set base URL
        url = "https://www.gesetze-im-internet.de"

        # Set default HTML file
        file = f'__{data["norm"]}.html'

        # Except for the 'Grundgesetz' ..
        if identifier == "gg":
            # .. which is different
            file = f'art_{data["norm"]}.html'

        # Combine everything
        return f'{url}/{self.library[identifier]["slug"]}/{file}'
