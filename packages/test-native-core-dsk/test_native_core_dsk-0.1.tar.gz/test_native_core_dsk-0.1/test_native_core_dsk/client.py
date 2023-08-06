from .session import SwapSession


class SwapApi:
    """
    Swap API Wrapper Class

    """

    def __init__(
        self,
        host: str,
        api_key: str,
    ):
        """Initialize the dnaCenterApi class object.  dnaCenterAPI
        provides an interface to the REST API of Cisco DNA Center

        Args:
            host (str): IP Address or Fully Qualified Domain Name of the DNA
                Center Appliance
            username (str): username is used for initial Basic Auth
            password (str): password
            verify (bool, optional): Certificate verification flag.
                Defaults to True.
        """
        self.session = SwapSession()
        self.session.add_api_key(api_key)
        self.host = host
        self.base_url = f"http://{host}"

    def _build_url(self, resource: str) -> str:
        """Generate the full URL based on the self.base_url plus the provided
        resource (API endpoint)

        Args:
            resource (str): API Endpoint suffix as found in the API documentation

        Returns:
            str: Full URL for API call
        """
        return self.base_url + resource

    def _make_request(
        self, method: str, url: str, json: dict = None, params: dict = None
    ):
        """Execute the request method of the Session object

        Args:
            method (str): HTTP Method passed to the session object
                [ GET, POST, PUT, PATCH, DELETE ]
            url (str): Full URL of the API endpoint
            json (dict, optional): Body if required. Defaults to None.
            params (dict, optional): [description]. Defaults to None.

        Returns:
            [type]: [description]
        """

        results = self.session.request(method, url, json=json, params=params)

        if results.ok:
            return results.json()

        results.raise_for_status()

    # API Endpoints

    def get_instruments(self) -> dict:
        """Retrieve all instruments

        Args:
            params (dict, optional): query parameters to filter the results.
            Defaults to None.

        Returns:
            dict: dictionary of the response
        """
        resource = "/instruments"
        params = {}
        return self._make_request("GET", self._build_url(resource), params=params)

    def get_indicative_quote(self, venue, chain, pair, side, amount, address) -> dict:
        """Retrieve all instruments

        Args:
            params (dict, optional): query parameters to filter the results.
            Defaults to None.

        Returns:
            dict: dictionary of the response
        """
        resource = f"/indicative-quote/{venue}/{chain}/{pair}/{side}/{amount}/{address}"
        params = {}
        return self._make_request("GET", self._build_url(resource), params=params)

    def get_firm_quote(self, venue, chain, pair, side, amount, address) -> dict:
        """Retrieve all instruments

        Args:
            params (dict, optional): query parameters to filter the results.
            Defaults to None.

        Returns:
            dict: dictionary of the response
        """

        resource = f"/firm-quote/{venue}/{chain}/{pair}/{side}/{amount}/{address}"
        params = {}
        return self._make_request("GET", self._build_url(resource), params=params)

    def get_allowance(self, token, address) -> dict:
        """Retrieve all instruments

        Args:
            params (dict, optional): query parameters to filter the results.
            Defaults to None.

        Returns:
            dict: dictionary of the response
        """
        resource = f"/allowance/{token}/{address}"
        params = {}
        return self._make_request("GET", self._build_url(resource), params=params)

    def get_balance(self, token, address) -> dict:
        """Retrieve all instruments

        Args:
            params (dict, optional): query parameters to filter the results.
            Defaults to None.

        Returns:
            dict: dictionary of the response
        """
        resource = f"/balance/{token}/{address}"
        params = {}
        return self._make_request("GET", self._build_url(resource), params=params)
