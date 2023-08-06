from ._requests import Requests


class Client:
    def __init__(self, auth):
        self.__requests = Requests(auth)

    async def getProfileList(self, limit=10, sort='FromMax', equal=False):
        data = {'limit': limit, 'sort': sort, 'equal': equal}
        response = await self.__requests.send_request('getProfileList', data)
        if response.get('status') == 'OK':
            return response.get('data').get('profiles')

    async def requestFollow(self, followee_id, profile_id, action='Follow'):
        data = {'f_type': action, 'followee_id': followee_id, 'profile_id': profile_id}
        response = await self.__requests.send_request('requestFollow', data)
        if response.get('status') == 'OK':
            return response.get('data')