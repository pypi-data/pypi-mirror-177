from requests import Response, get, post, delete, put

from .models import *


class TradeAnalyzerClient:

    BASE_URL: str = 'http://127.0.0.1:8000'

    __access_token: str = ''

    @classmethod
    def login(cls, username: str, password: str):
        endpoint: str = '/login'

        json_data = {
            'username': username,
            'password': password
        }
        response: Response = post(cls.BASE_URL + endpoint, json = json_data, headers = {
            'Content-Type': 'application/json'
        })
        return response

    @classmethod
    def create_strategy(cls, id: str, description: str, type: StrategyType, commission_model: CommissionModel, platform: Platform, currency: str):
        endpoint: str = '/api/v1/strategy'

        json_data = {
            'id': id,
            'description': description,
            'type': type.value,
            'commission_model': commission_model.commission_rule.value,
            'commission_pricing': commission_model.pricing,
            'platform': platform.value,
            'currency': currency
        }
        
        response: Response = post(cls.BASE_URL + endpoint, json = json_data, headers = {
            'Content-Type': 'application/json'
        })
        return response

    @classmethod
    def get_strategies(cls):
        endpoint: str = '/api/v1/strategy'
        response: Response = get(cls.BASE_URL + endpoint, headers = {
            'Content-Type': 'application/json'
        }) 
        return response

    @classmethod
    def get_strategy(cls, strategy_id: str):
        endpoint: str = '/api/v1/strategy'
        json_data = {
            'id': strategy_id
        }

        response: Response = get(cls.BASE_URL + endpoint, json = json_data, headers = {
            'Content-Type': 'application/json'
        }) 
        return response

    @classmethod
    def delete_strategy(cls, strategy_id: str):
        endpoint: str = '/api/v1/strategy'
        json_data = {
            'id': strategy_id
        }

        response: Response = delete(cls.BASE_URL + endpoint, json = json_data, headers = {
            'Content-Type': 'application/json'
        }) 
        return response

    