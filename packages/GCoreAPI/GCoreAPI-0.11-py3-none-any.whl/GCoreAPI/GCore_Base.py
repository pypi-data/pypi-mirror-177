import requests


class Base:
    BASE_URL = 'https://api.edgecenter.ru/cloud/v1'

    def __init__(self, token: str, project_id: int):
        self.token = token
        self.project_id = project_id
        self.headers = {'Authorization': f'APIKey {self.token}'}
        self.body = None
        self.data = None
        self.cookies = None
        self.error_desc = None

    def reset(self):
        self.body = None
        self.data = None
        self.cookies = None
        self.headers = {'Authorization': f'APIKey {self.token}'}

    def add_cookie(self, key, value):
        if self.cookies is None:
            self.cookies = {}
        self.cookies.update({key: value})

    def add_query_param(self, key, value):
        if self.data is None:
            self.data = {}
        self.data.update({key: value})

    def add_application_header(self) -> None:
        self.headers.update({'Content-Type': 'application/json'})

    def add_to_json(self, key, value) -> None:
        if self.body is None:
            self.body = {}
        self.body.update({key: value})

    def request(self, url, params=None, body=None, cookies=None, request_type: str = 'GET') -> dict:

        requests_types = {
            'GET': requests.get,
            'POST': requests.post,
            'PUT': requests.put,
            'DELETE': requests.delete,
            'PATCH': requests.patch,
        }

        try:
            data = self.data if params is not None else None
            json = self.body if body is not None else None
            cookies = self.cookies if cookies is not None else None

            response = requests_types[request_type](url=url,
                                                    headers=self.headers,
                                                    json=json,
                                                    data=data,
                                                    cookies=cookies)
            if response.status_code in (200, 201, 204):
                return response.json()
            elif response.status_code == 401:
                print("UnauthorizedError", response.json()['message'])
        except Exception as err:
            self.error_desc = err

        print(f"Request ERROR: {self.error_desc}")
        return {}
