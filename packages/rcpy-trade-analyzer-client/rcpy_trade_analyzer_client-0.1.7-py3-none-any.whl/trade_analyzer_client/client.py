from typing import List

import requests
from requests import Response

from .models import Strategy

class TradeAnalyzerClient:
    
    BASE_URL: str = 'http://127.0.0.1:8000'

    @classmethod
    def register(cls, username: str, email: str, full_name: str, password: str) -> Response:
        url: str = cls.BASE_URL + '/register'
        json_data = {
            'username': username,
            'email': email,
            'full_name': full_name,
            'password': password
        }
        return requests.post(url, json = json_data, headers = {
            'Content-Type': 'application/json'
        })

    @classmethod
    def login(cls, username: str, password: str) -> Response:
        url: str = cls.BASE_URL + '/login'
        json_data = {
            'username': username,
            'password': password
        }
        return requests.post(url, json = json_data, headers = {
            'Content-Type': 'application/json'
        })

    @classmethod
    def get_strategies(cls) -> List[Strategy]:
        strategies: List[Strategy] = []

        url: str = cls.BASE_URL + '/api/v1/strategies'

        response: Response = requests.get(url, headers = {
            'Content-Type': 'application/json'
        })
        
        return strategies