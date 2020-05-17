import requests
import time
from tenacity import retry, stop_after_delay, wait_fixed
from decouple import config

from .api_access import BaseApiAccess


class TrueLayer_API(BaseApiAccess):

    base_url = 'https://api.truelayer.com'


    auth_url = 'https://auth.truelayer.com'
    auth_endpoint = '/connect/token'

    accounts_endpoint = '/data/v1/accounts'


    def _request_token(self, username: str, password: str):
        """
        Request an authentication token from the server
        :return: the token or None if the response did not contain a token
        """

        values_token = {
            "grant_type": "authorization_code",
            "client_id": config('TRUELAYER_CLIENT_ID'),
            "client_secret": config('TRUELAYER_CLIENT_SECRET'),
            "redirect_uri": "https://console.truelayer.com/redirect-page",
            "code": "",
        }

        response = requests.post(self.auth_url + self.auth_endpoint, data=values_token, headers=self.auth_headers)
        response.raise_for_status()
        
        return response

    
    def _request_refresh_token(self, refresh_token: str):
        """
        Refreshes an authentication token
        :param refresh_token: the refresh token issued by the server when requesting a token
        :return: the refreshed token data
        """

        print("Requesting token refresh using refresh_token {}".format(refresh_token))

        values_token = {
            'grant_type': 'refresh_token',
            "client_id": config('TRUELAYER_CLIENT_ID'),
            "client_secret": config('TRUELAYER_CLIENT_SECRET'),
            'refresh_token': refresh_token,
        }

        response = requests.post(self.auth_url + self.auth_endpoint, data=values_token, headers=self.auth_headers)
        response.raise_for_status()
        
        return response.json()


    def get_transactions(self, sub_accounts=[], first_import_success=False, last_import=None):
        """
        Get a list of transactions.
        :param sub_accounts: list with queryset of Sub-Accounts
        :param first_import_success: True if initial import with all transactions has been conducted, otherwise false
        :param last_import: date of last import in datetime format
        :return: list of transactions as returned by api
        """

        transactions = []

        # get transactions for each sub_account
        for sub_account in sub_accounts:

            transactions_endpoint = '/data/v1/accounts/{}/transactions'.format(sub_account.provider_subaccount_id)

            sub_account_transactions = self._do_request(self.GET, transactions_endpoint)['results']

            transactions.extend(sub_account_transactions)
            
        return transactions

        # return self._do_request(GET, self.transactions_endpoint)



class N26_API(BaseApiAccess):

    base_url = 'https://api.tech26.de'
    
    auth_url = 'https://api.tech26.de'
    auth_endpoint = "/oauth/token"
    auth_headers = {
        "Authorization": "Basic bXktdHJ1c3RlZC13ZHBDbGllbnQ6c2VjcmV0"
    }
    mfa_required = True
    
    request_endpoint = None
    request_headers = None
    user_agent = ("Mozilla/5.0 (X11; Linux x86_64) "
              "AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/59.0.3071.86 Safari/537.36")


    # transactions_endpoint = '/api/smrt/transactions?limit=100'
    transactions_endpoint = '/api/smrt/transactions?from=1325372400000&to={}&limit=5000'.format(int(round(time.time() * 1000)))
    accounts_endpoint = '/api/spaces'


    def _request_mfa_approval(self, response):
        """

        """
        
        if response.status_code != 403:
            raise ValueError("Unexpected response for initial auth request: {}".format(response.text))


        response_data = response.json()
        
        if response_data.get("error", "") == "mfa_required":
            mfa_token = response_data["mfaToken"]
        else:
            raise ValueError("Unexpected response data")


        print("Requesting MFA approval using mfa_token {}".format(mfa_token))

        mfa_data = {
            'mfaToken': mfa_token,
            'challengeType': 'oob',
        }

        mfa_response = requests.post(
            self.auth_url + '/api/mfa/challenge',
            json=mfa_data,
            headers={
                **self.auth_headers,
                # "User-Agent": USER_AGENT,
                'Content-Type': 'application/json'
        })

        mfa_response.raise_for_status()

        # return tokens
        return self._complete_authentication_flow(mfa_token)



    @retry(wait=wait_fixed(5), stop=stop_after_delay(60))
    def _complete_authentication_flow(self, mfa_token: str) -> dict:
        """
        Wait until login is confirmed by user, then get tokens and return them
        """

        print("Completing authentication flow for mfa_token {}".format(mfa_token))
        
        mfa_response_data = {
            'mfaToken': mfa_token,
            'grant_type': 'mfa_oob'
        }

        response = requests.post(self.auth_url + '/oauth/token', data=mfa_response_data, headers=self.auth_headers)
        response.raise_for_status()
        tokens = response.json()
        return tokens


"""
Export provider classes
"""

api_providers = {
    'n26_DE': N26_API,
    'revolut_DE': TrueLayer_API,
}