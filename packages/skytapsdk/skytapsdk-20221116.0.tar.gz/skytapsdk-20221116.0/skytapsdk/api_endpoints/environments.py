"""Environments Class for calling "configurations" API endpoints."""
from restfly.endpoint import APIEndpoint

from skytapsdk.helpers import links_iterator


class Environments(APIEndpoint):
    """
    "configurations" API endpoint

    API Doc Reference: https://help.skytap.com/API_v2_Documentation.html#Configur
    """

    _path = "configurations"

    def get_all(self, **kwargs) -> list:
        """
        Get all environment records based on query parameters sent in kwargs.

        API Doc Reference: https://help.skytap.com/API_v2_Documentation.html#Getallenvironments

        Returns:
            list of all environments, per set params in kwargs.
        """
        return links_iterator(api=self._api, path=self._path, **kwargs)

    def get_by_id(self, uid: int) -> dict:
        """
        GET a specific environment.

        API Doc Reference: https://help.skytap.com/API_v2_Documentation.html#Getenvironment

        Args:
            uid: ID of desired environment.

        Returns:
            dict of queried environment.
        """
        self._path = f"{self._path}/{uid}"
        return self._get().json()
