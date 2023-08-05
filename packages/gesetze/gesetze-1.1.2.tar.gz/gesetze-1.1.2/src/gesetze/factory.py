"""
This module is part of the 'py-gesetze' package,
which is released under GPL-3.0-only license.
"""

# pylint: disable=R0903

from .drivers import Buzer, DejureOnline, Driver, GesetzeImInternet, Lexparency


class Factory:
    """
    Utilities for creating 'Driver' instances
    """

    @staticmethod
    def create(driver: str) -> Driver:
        """
        Creates a new 'Driver' instance for the given type

        :param driver: str Driver type
        :return: Driver Driver instance
        :raises: Exception Invalid driver type
        """

        # List available drivers
        drivers = {
            # (1) 'gesetze-im-internet.de'
            "gesetze": GesetzeImInternet,
            # (2) 'dejure.org'
            "dejure": DejureOnline,
            # (3) 'buzer.de'
            "buzer": Buzer,
            # (4) 'lexparency.de'
            "lexparency": Lexparency,
        }

        # Fail early for invalid drivers
        if driver not in drivers:
            raise Exception(f'Invalid driver type: "{driver}"')

        # Instantiate object
        return drivers[driver]()
