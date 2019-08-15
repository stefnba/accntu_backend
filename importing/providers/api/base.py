import requests


class BaseApiAccess(object):

    url = None
    auth_endpoint = None

    def __init__(self, username, password):
        
        self.access_token = None
        self.transactions = []

        login = self.login(username, password)
        if login:
            self.transactions = self.get_transactions()


    def login(self, username, password):

        data = {'grant_type': 'password', 'username': username, 'password': password}
        headers = {'Authorization': 'Basic YW5kcm9pZDpzZWNyZXQ='}

        r = requests.post(self.url + self.auth_endpoint, data=data, headers=headers)
        if r.status_code == 200:
            self.access_token = str(r.json()['access_token'])
            return True

        else:
            return False


    def get_transactions(self):
        headers = {'Authorization': 'bearer' + self.access_token}

        r = requests.get(self.url + '/api/smrt/transactions', headers=headers)

        if r.status_code == 200:
            return r.json()
        else:
            return []


    def return_transactions(self):
        nmbr_transactions = len(self.transactions)
        if  nmbr_transactions > 0:
            print('{} transactions retrieved with {}'.format(nmbr_transactions, self.__class__.__name__))
            return self.transactions

        else:
            # TODO error handling
            print('{} failed to retrieve any transactions'.format(self.__class__.__name__))