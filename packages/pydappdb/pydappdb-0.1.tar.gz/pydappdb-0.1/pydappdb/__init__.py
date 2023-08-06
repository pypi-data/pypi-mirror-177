import requests
import json

class DappDb:
    def __init__(self, username, api_key):
        self.username = username
        self.api_key = api_key

    def authUser(self):
        url = 'http://127.0.0.1:8000/blocks/authUser'

        payload = {
            'cudder_username': self.username,
            'cudder_api_key': self.api_key
        }
        try:
            r = requests.post(url, data=payload)
            r = r.json()
        except:
            return {'status': False, 'message': 'json error'}

        if r['auth']:
            cudder_username = r['cudder_username']
            cudder_api_key = r['cudder_api_key']

            return {'status': True, 'cudder_username': cudder_username, 'cudder_api_key': cudder_api_key}

        else:
            return {'status': False, 'message': 'json error'}

    def dappset(self, data_key, data_value):
        url = 'http://127.0.0.1:8000/blocks/storeData'

        payload = {
            'key': data_key,
            'value': data_value,
            'cudder_username': self.username,
            'cudder_api_key': self.api_key
        }

        r = requests.post(url, data=payload)
        r = r.json()
        print(r)

    # fetch blocks
    def dappget(self):
        fetch_url = 'http://127.0.0.1:8000/blocks/get_user_data_blocks'

        payload = {
            'cudder_username': self.username,
            'cudder_api_key': self.api_key
        }

        r = requests.post(fetch_url, data=payload)
        r = r.json()

        print(r)
        print(len(r))
