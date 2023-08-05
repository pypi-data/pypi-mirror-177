"""Assets Class for calling "assets" API endpoints."""
from restfly.endpoint import APIEndpoint

from skytapsdk.helpers import links_iterator


class Assets(APIEndpoint):
    """
    "assets" API endpoint

    API Doc Reference: https://help.skytap.com/API_v2_Documentation.html#Asset
    """

    _path = "assets"

    def get_all(self, **kwargs) -> list:
        """
        Get all asset records based on query parameters sent in kwargs.

        API Doc Reference: https://help.skytap.com/API_v2_Documentation.html#Listassets

        Returns:
            list of all assets, per set params in kwargs.
        """
        return links_iterator(api=self._api, path=self._path, **kwargs)

    def get_by_id(self, uid: int) -> dict:
        """
        GET a specific asset.

        API Doc Reference: https://help.skytap.com/API_v2_Documentation.html#Operationsonassets

        Args:
            uid: ID of desired asset.

        Returns:
            dict of queried asset.
        """
        self._path = f"{self._path}/{uid}"
        return self._get().json()
