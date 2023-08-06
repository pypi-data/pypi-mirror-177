"""Reports Class for calling "reports" API endpoints."""
import time

from restfly.endpoint import APIEndpoint


class Reports(APIEndpoint):
    """
    "reports" API endpoint

    API Doc Reference: https://help.skytap.com/API_v2_Documentation.html#Usage
    """

    _path = "reports"
    _query_delay = 5  # sleep seconds.

    def get_report(self, **kwargs) -> dict:
        """
        Get all user records based on query parameters sent in kwargs.

        API Doc Reference: https://help.skytap.com/API_v2_Documentation.html#Usage

        Returns:
             list of all user accounts, per set params in kwargs.
        """
        # Post the Report request.
        self._path = f"{self._path}.json"

        result = self._post(json=kwargs).json()

        # Query the API to check if the report is built.
        self._path = f"{self._path.split('.')[0]}/{result['id']}.json"
        while result["ready"] is not True:
            print(f"Ready: {result['ready']} for Job ID: {result['id']}.")
            result = self._get().json()
            time.sleep(kwargs.get('query_delay', self._query_delay))
        return result
