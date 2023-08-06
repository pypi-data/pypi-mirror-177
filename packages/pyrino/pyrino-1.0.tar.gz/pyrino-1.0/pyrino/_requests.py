from urllib3 import PoolManager
from ujson import dumps, loads
from .exceptions import *

class Requests:
    def __init__(self, auth):
        if len(auth) != 32: raise ValueError('your AUTH is incorrect, please check and try again')
        self.__auth = auth
        self.__platform_client = {'app_name': 'Main', 'app_version': '3.0.7', 'platform': 'Android', 'package': 'app.rbmain.a', 'lang_code': 'fa' }
        self.__url = 'https://rubino1.iranlms.ir/'
        self.__pool_manager = PoolManager()
        self.__header = {'Content-Type': 'application/json'}

    async def send_request(self, method, data):
        data = {
            'api_version': '0',
            'auth': self.__auth,
            'client': self.__platform_client,
            'data': data,
            'method': method
        }
        data = dumps(data).encode('utf-8')
        while True:
            response = self.__pool_manager.request('POST', self.__url, body=data, headers=self.__header)
            if not response.status == 200:
                continue
            else:
                result = loads(response.data.decode('utf-8'))
                if result.get('status') == 'ERROR_ACTION':
                    if result.get('status_det'):
                        raise USERNAME_NOT_EXIST('Your account does not have a username, please enter a username for your account and try again')
                else:
                    return result