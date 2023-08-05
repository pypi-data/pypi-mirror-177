"""
This module is part of the 'py-gesetze' package,
which is released under GPL-3.0-only license.
"""

# pylint: disable=R0801

from .driver import Driver


class DejureOnline(Driver):
    """
    Utilities for dealing with 'dejure.org'
    """

    # Individual identifier
    identifier: str = "dejure"

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
        url = "https://dejure.org/gesetze"

        # Set HTML file
        file = f'{data["norm"]}.html'

        # Combine everything
        return f'{url}/{self.library[identifier]["slug"]}/{file}'
