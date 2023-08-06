"""platform.py."""
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

from gql import Client, gql
from gql.transport.exceptions import TransportQueryError

from sw_product_lib.error import StrangeworksError
from sw_product_lib.transport import StrangeworksTransport


DEFAULT_PLATFORM_BASE_URL = "https://api.strangeworks.com"
PLATFORM_PRODUCT_PATH = "products"


ALLOWED_HEADERS = {""}


class Operation:
    """Object for definining requests made to the platform."""

    def __init__(
        self,
        query: str,
        allowed_vars: Optional[List[str]] = None,
        upload_files: bool = False,
    ) -> None:
        """Initialize object

        Accepts a GraphQL query or mutation as a string. Derives variable names used by
        the query if none were provided.

        Parameters
        ----------
        query: str
            a GraphQL query or mutation as string.
        allowed_vars: Optional[List[str]]
            list to override which variables can be sent was part of query.
        """
        self.query = gql(query)
        self.allowed_vars = (
            allowed_vars
            if allowed_vars
            else list(
                map(
                    lambda x: x.variable.name.value,
                    self.query.definitions[0].variable_definitions,
                )
            )
        )
        self.upload_files = upload_files

    def variables(
        self, values: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:

        if not self.allowed_vars:
            return values

        vars = {}
        for k, v in values.items():
            if k in self.allowed_vars and v is not None:
                vars[k] = v
        return vars


class API:
    """Client for Platform API."""

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        auth_token: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        """Initialize platform API client.

        Provides access to the platform API methods which allows products to interact
        with the Strangeworks platform.

        Parameters
        ----------
        auth_token: str
            jwt token used to authorize requests to the platform API's.
        platform_url: str
            Base url for accessing the platform API. Defaults to
            https://api.strangeworks.com
        headers: Dict[str, str]
            Additional values to set in the header for the request. The header must
            belong to ALLOWED_HEADERS.
        """
        self.api_key: str = api_key
        self.products_api_url = urljoin(
            base_url or DEFAULT_PLATFORM_BASE_URL, PLATFORM_PRODUCT_PATH
        )
        # add auth token into api
        transport = StrangeworksTransport(
            base_url=self.products_api_url, api_key=self.api_key
        )
        self.gql_client = Client(transport=transport)
        transport.connect()
        self.auth_token = transport.auth_token

    def execute(self, op: Operation, **kvargs):
        """Execute an operation on the platform.
        Parameters
        ----------
        op: Operation
            which request to run
        variable_values; Optional[Dict[str, Any]]
            values to send with the request
        """
        try:
            result = self.gql_client.execute(
                document=op.query,
                variable_values=op.variables(kvargs),
                upload_files=op.upload_files,
            )
            return result
        except TransportQueryError as e:
            print(f"error during query: {e}")
            raise StrangeworksError.server_error(e)
