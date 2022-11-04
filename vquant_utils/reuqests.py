import aiohttp
import requests


class RequestMethod:
    GET, POST, PUT, DELETE = 'GET', 'POST', 'PUT', 'DELETE'


class Requests:
    @staticmethod
    def requests(method, url, **kwargs):
        response = requests.request(method, url ** kwargs)
        try:
            res = response.json()
        except Exception:
            raise TypeError(response.text)
        else:
            return res

    @staticmethod
    async def async_requests(method, url, **kwargs):
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, **kwargs) as response:
                try:
                    response = await response.json()
                except Exception:
                    response = await response.text()
                    raise TypeError(response)
                else:
                    return response
