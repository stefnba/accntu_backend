import requests


class BaseApiAccess(object):

    url = None
    auth_endpoint = None

    def __init__(self):
        
        self.access_token = None


    def login(self, username, password, login_sec):

        data = {'grant_type': 'password', 'username': username, 'password': password}
        headers = {'Authorization': 'Basic YW5kcm9pZDpzZWNyZXQ='}

        r = requests.post(self.url + self.auth_endpoint, data=data, headers=headers)
        if r.status_code == 200:
            self.access_token = str(r.json()['access_token'])
            return True

        else:
            return False


    def get_raw_transactions(self, **kwargs):
        headers = {'Authorization': 'bearer' + self.access_token}

        r = requests.get(self.url + '/api/smrt/transactions', headers=headers)

        if r.status_code == 200:
            return r.json()
        else:
            return []