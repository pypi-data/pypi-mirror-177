"""Users Class for calling "users" API endpoints."""
from restfly.endpoint import APIEndpoint

from skytapsdk.helpers import links_iterator


class Users(APIEndpoint):
    """
    "users" API endpoint

    API Doc Reference: https://help.skytap.com/API_v2_Documentation.html#User2
    """

    _path = "users"

    def get_all(self, **kwargs) -> list:
        """
        Get all user records based on query parameters sent in kwargs.

        API Doc Reference: https://help.skytap.com/API_v2_Documentation.html#Listusers

        Returns:
            list of all user accounts, per set params in kwargs.
        """
        return links_iterator(api=self._api, path=self._path, **kwargs)

    def get_by_id(self, uid: int) -> dict:
        """
        GET a specific user.

        API Doc Reference: https://help.skytap.com/API_v2_Documentation.html#User2

        Args:
            uid: ID of desired user.

        Returns:
            dict of queried user account.
        """
        self._path = f"{self._path}/{uid}"
        return self._get().json()
