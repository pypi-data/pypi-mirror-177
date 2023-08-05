import json
from requests import Session, Response
from urllib.parse import urljoin
if __package__:
    from .exceptions import *
else:
    from exceptions import *


class EdithSession(Session):

    def __init__(self, base_url, token, **kwargs):
        self.base_url = base_url
        self.debug = kwargs.get('debug', False)
        super(EdithSession, self).__init__()
        self.headers = {'Authorization': 'token ' + token}

    def verify_response(self, response: Response, expcted_status_code: int = 200):
        if not response.status_code == expcted_status_code:
            if self.debug:
                print('Unexpected status code:', response.status_code)
                # print(response.content)
            if response.status_code == 401:
                raise EdithUnauthorizedAction()
            if response.status_code == 500:
                raise EdithInternalError()
            if response.status_code == 400:
                raise EdithInputError(json.dumps(response.json()))
            if response.status_code == 404:
                raise EdithResourceNotFound()
        return response.json()

    def request(self, method, url, *args, **kwargs):
        url = urljoin(self.base_url, url)
        headers = kwargs.get('headers', {})
        kwargs['headers'] = headers.update(self.headers)
        return super(EdithSession, self).request(method, url, *args, **kwargs)

    def get(self, url, **kwargs):
        url = urljoin(self.base_url, url)
        resp = self.request('GET', url, **kwargs)
        return self.verify_response(resp, expcted_status_code=200)

    def post(self, url, data=None, json=None, **kwargs):
        url = urljoin(self.base_url, url)
        resp = self.request('POST', url, data=data, json=json, **kwargs)
        return self.verify_response(resp, expcted_status_code=201)

    def patch(self, url, data=None, **kwargs):
        url = urljoin(self.base_url, url)
        resp = self.request('PATCH', url, data=data, **kwargs)
        return self.verify_response(resp, expcted_status_code=200)
