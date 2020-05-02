import requests
import time
from datetime import datetime, timedelta
from requests import HTTPError

from accounts.models import Token_Data

GET = "get"
POST = "post"

EXPIRATION_TIME_KEY = "expires_at"
CREATION_TIME_KEY = "created_at"
ACCESS_TOKEN_KEY = "access_token"
REFRESH_TOKEN_KEY = "refresh_token"

GRANT_TYPE_PASSWORD = "password"
GRANT_TYPE_REFRESH_TOKEN = "refresh_token"





class BaseApiAccess(object):
    """
    Api class can be imported as a library in order to use it within applications
    """

    base_url = None
    
    auth_url = None
    auth_endpoint = None
    auth_headers = None
    mfa_required = False
    
    request_endpoint = None
    request_headers = None
    user_agent = None


    transactions_endpoint = None
    accounts_endpoint = None


    def __init__(self, account_id, username, password):
        
        self.account_id = account_id
        self.username = username
        self.password = password
        
        self.is_authenticated = False
        self.token_data = None


    def get_transactions(self):
        """
        Get a list of transactions.
        """

        return self._do_request(GET, self.transactions_endpoint)


    def get_accounts(self):
        """
        Retrieves basic account information
        """

        return self._do_request(GET, self.accounts_endpoint)




    def _do_request(
                self, 
                method: str = GET,
                url: str = "/",
                params: dict = None,
                data: dict = None
    ) -> list or dict or None:
        """
        Executes a http request based on the given parameters
        :param method: the method to use (GET, POST)
        :param url: the url to use
        :param params: query parameters that will be appended to the url
        :param json: request body
        :return: the response parsed as a json
        """
        
        access_token = self.get_access_token()

        if not access_token:
            return []


        headers = {'Authorization': 'Bearer {}'.format(access_token)}

        url = self.base_url + url

        # do api call
        if method is GET:
            response = requests.get(url, headers=headers, json=data)
        elif method is POST:
            response = requests.post(url, headers=headers, json=data)
        else:
            raise ValueError("Unsupported method: {}".format(method))


        response.raise_for_status()
        
        # some responses do not return data so we just ignore the body in that case
        if len(response.content) > 0:
            return response.json()

    
    def get_access_token(self) -> str or None:
        """
        :return: access token as string
        """

        auth_status = self.check_auth_status()

        print('Auth_status: {}'.format(auth_status))

        if auth_status == "AUTHENTICATED":
            print('Account already authenticated')

        if auth_status == "REFRESH_AUTH_REQUIRED":
            self.refresh_authentication()

        if auth_status == "NOT_AUTHENTICATED":
            self.new_authentication()


        return self.token_data[ACCESS_TOKEN_KEY]


    def check_auth_status(self):
        """

        """

        if not self.token_data:
            self.token_data = self._retrieve_token_from_db(self.account_id)

        # if no token in db
        if not self.token_data:
            return "NOT_AUTHENTICATED"

        # validate 
        if self._validate_token(self.token_data):
            return "AUTHENTICATED"
        else:
            return "REFRESH_AUTH_REQUIRED"


    def new_authentication(self):
        """

        """

        username = self.username
        password = self.password

        # start token request, token data will be returned
        print('Starting new auth process for {}'.format(username))
        token_data = self._request_token(username, password)

        self.set_token(token_data)


    def _request_token(self, username: str, password: str):
        """
        Request an authentication token from the server
        :return: the token or None if the response did not contain a token
        """

        values_token = {
            "grant_type": GRANT_TYPE_PASSWORD,
            "username": username,
            "password": password
        }

        response = requests.post(self.base_url + self.auth_endpoint, data=values_token, headers=self.auth_headers)
        
        # do mfa approval if applicable
        if self.mfa_required:
            return self._request_mfa_approval(response)


    def _request_mfa_approval(self, response):
        """
        Must be overwritten by actual API Class
        """
        pass


    def refresh_authentication(self):
        """
        Refreshes an existing authentication using a (possibly expired) token.
        :raises AssertionError: if no existing token data was found
        :raises PermissionError: if the token is invalid even after the refresh
        """

        token_data = self.token_data

        if REFRESH_TOKEN_KEY in token_data:
            print("Trying to refresh existing token")
            refresh_token = token_data[REFRESH_TOKEN_KEY]

            try:
                token_data = self._request_refresh_token(refresh_token)
                self.set_token(token_data)

            except HTTPError as http_error:
                if http_error.response.status_code == 401:
                    self.new_authentication()
                else:
                    raise http_error

        else:
            raise AssertionError("Cant refresh token since no existing token data was found. "
                                 "Please initiate a new authentication instead.")        


    def _request_refresh_token(self, refresh_token: str):
        """
        Refreshes an authentication token
        :param refresh_token: the refresh token issued by the server when requesting a token
        :return: the refreshed token data
        """

        print("Requesting token refresh using refresh_token {}".format(refresh_token))

        values_token = {
            'grant_type': GRANT_TYPE_REFRESH_TOKEN,
            'refresh_token': refresh_token,
        }

        print(values_token)

        response = requests.post(self.base_url + self.auth_endpoint, data=values_token, headers=self.auth_headers)
        response.raise_for_status()
        return response.json()


    def set_token(self, token_data):
        """
        Validates newly received token, adds expiration datetime and calls method to save in db
        :param refresh_token: the refresh token issued by the server when requesting a token
        """

        print("Token Data", token_data)

        # add expiration time to expiration in _validate_token()
        now = datetime.now()
        token_data[CREATION_TIME_KEY] = str(now)
        token_data[EXPIRATION_TIME_KEY] = str(now + timedelta(seconds=token_data["expires_in"]))

        # if it's still not valid, raise an exception
        if not self._validate_token(token_data):
            raise PermissionError("Unable to request authentication token")


        # authentication successful
        else:
            print(token_data)

            self._save_token_to_db(token_data, self.account_id)

            self.token_data = token_data


    @staticmethod
    def _validate_token(token_data: dict) -> bool:
        """
        Checks if a token is valid
        :param token_data: the token data to check
        :return: true if valid, false otherwise
        """
        
        if EXPIRATION_TIME_KEY not in token_data:
            # there was a problem adding the expiration_time property
            return False
        
        elif datetime.now() >= datetime.strptime(token_data[EXPIRATION_TIME_KEY], '%Y-%m-%d %H:%M:%S.%f'):
            
            # Token has expired
            print('Token has expired')
            return False

        return ACCESS_TOKEN_KEY in token_data and token_data[ACCESS_TOKEN_KEY]


    @staticmethod
    def _retrieve_token_from_db(account_id: int) -> dict or None:
        """
        Get token from database
        :return: access token
        """
        
        token = Token_Data.objects.filter(account_id=account_id).order_by('-created_at').first()

        if token:
            return {
                'access_token': token.access_token,
                'refresh_token': token.refresh_token,
                EXPIRATION_TIME_KEY: str(token.expires_at),
            }


    @staticmethod
    def _save_token_to_db(token_data, account_id):
        """
        Saves token data and timestamp to database
        """

        token_data = {
            **token_data,
            'raw_token_data': token_data,
            'account_id': account_id,
        }
        
        saved_token = Token_Data.objects.create(**token_data)