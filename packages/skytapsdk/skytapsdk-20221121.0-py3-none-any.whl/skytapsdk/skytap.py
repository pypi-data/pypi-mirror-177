import logging

from restfly.session import APISession

from skytapsdk.api_endpoints.assets import Assets
from skytapsdk.api_endpoints.environments import Environments
from skytapsdk.api_endpoints.templates import Templates
from skytapsdk.api_endpoints.users import Users


class Skytap(APISession):
    """A controller to access Endpoints in the Skytap API."""

    BASE_URL = "https://cloud.skytap.com"
    API_VERSION = 1

    def __init__(
        self,
        username: str = None,
        password: str = None,
        token: str = None,
        **kwargs,
    ):
        """
        Create a Skytap object for managing interactions with the Skytap API.

        Args:
            username: Username for API auth
            password: Password for API auth (optional)
            token: Token for API auth (preferred over password)
            kwargs: Various settable values
                api_version (int) Defaults to self.API_VERSION.
        """

        self._username = username
        self._password = password
        self._token = token
        self._api_version = self.API_VERSION
        self._url = self.BASE_URL

        # Use setter to update the self._api_version AND rewrite the self._url.
        self.api_version = kwargs.get("api_version", self.API_VERSION)
        super(Skytap, self).__init__(
            username=self._username,
            password=self._password,
            token=self._token,
            **kwargs,
        )
        self.login()

    def login(self):
        if self._username:
            if self._token:
                self._session.auth = (self._username, self._token)
            elif self._password:
                self._session.auth = (self._username, self._password)
            else:
                logging.warning("Token or Password is required for authentication.")
        self._session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

    def logout(self):
        self._session.auth = None

    @property
    def api_version(self) -> int:
        return self._api_version

    @api_version.setter
    def api_version(self, version: int):
        """When api_version is updated you need to also update the self._url."""
        self._api_version = version
        self._url = self.BASE_URL
        if self._api_version == 2:
            self._url = f"{self._url}/v2"

    @property
    def users(self) -> Users:
        return Users(self)

    @property
    def configurations(self) -> Environments:
        return Environments(self)

    @property
    def environments(self) -> Environments:
        """
        Some people might find it easier to use 'configurations' by the name 'environments' since that is what they see in
        the UI.
        """
        return Environments(self)

    @property
    def templates(self) -> Templates:
        return Templates(self)

    @property
    def assets(self) -> Assets:
        return Assets(self)
