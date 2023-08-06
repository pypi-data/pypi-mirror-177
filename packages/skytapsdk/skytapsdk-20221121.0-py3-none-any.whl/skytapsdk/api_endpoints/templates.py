"""Templates Class for calling "templates" API endpoints."""
from restfly.endpoint import APIEndpoint

from skytapsdk.helpers import links_iterator


class Templates(APIEndpoint):
    """
    "templates" API endpoint

    API Doc Reference: https://help.skytap.com/API_v2_Documentation.html#Template
    """

    _path = "templates"

    def get_all(self, **kwargs) -> list:
        """
        Get all template records based on query parameters sent in kwargs.

        API Doc Reference: https://help.skytap.com/API_v2_Documentation.html#Getlistoftemplates

        Returns:
            list of all templates, per set params in kwargs.
        """
        return links_iterator(api=self._api, path=self._path, **kwargs)

    def get_by_id(self, uid: int) -> dict:
        """
        GET a specific template.

        API Doc Reference: https://help.skytap.com/API_v2_Documentation.html#Gettemplate

        Args:
            uid: ID of desired template.

        Returns:
            dict of queried template.
        """
        self._path = f"{self._path}/{uid}"
        return self._get().json()
