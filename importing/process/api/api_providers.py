import requests
from tenacity import retry, stop_after_delay, wait_fixed

from .api_access import BaseApiAccess


class N26_API(BaseApiAccess):

    base_url = 'https://api.tech26.de'
    
    auth_url = 'https://api.tech26.de'
    auth_endpoint = "/oauth/token"
    auth_headers = {"Authorization": "Basic bXktdHJ1c3RlZC13ZHBDbGllbnQ6c2VjcmV0"}
    mfa_required = True
    
    request_endpoint = None
    request_headers = None
    user_agent = ("Mozilla/5.0 (X11; Linux x86_64) "
              "AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/59.0.3071.86 Safari/537.36")


    transactions_endpoint = '/api/smrt/transactions'
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






api_providers = {
    'n26_DE': N26_API,
}