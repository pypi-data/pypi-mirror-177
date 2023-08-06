from time import sleep
from enum import Enum

from requests import Session, Response
from bs4 import BeautifulSoup


class HttpMethod(Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'


class SyncApiCollector:
    def __init__(self, main_api_link: str, main_params: str = None, cookie: dict = None):
        self.main_api_link = main_api_link
        self.main_api_params = main_params
        self.cookie = cookie
        self.session = Session()

    def push_request(self, method: str, http_method: HttpMethod, params: dict = None) -> Response:
        params = {**self.main_api_params,  **params}
        return self.session.request(http_method.value,
                                    f'{self.main_api_link}/{method}',
                                    cookies=self.cookie,
                                    params=params)

    def get_json_content(self, method: str, http_method: HttpMethod, params: dict = None) -> dict:
        return self.push_request(method, http_method, params).json()

    def get_html_content(self, method: str, http_method: HttpMethod, params: dict = None) -> BeautifulSoup:
        html = self.push_request(method, http_method, params).text
        return BeautifulSoup(html, 'html.parser')

    def get_until_http_code(self, method: str, http_method: HttpMethod,
                            limit: int = 5, time: float = 10,
                            params: dict = None, http_code: int = 200) -> Response | None:
        req = self.push_request(method, http_method, params)
        while req.status_code != http_code or limit != 0:
            req = self.get_until_http_code(method, http_method, limit-1, time, params, http_code)
            sleep(time)
        return req if req.status_code == http_code else None
