"""
-------------------------------------
-- Dexpresso.protocol: GeneralClient.py --
-------------------------------------
Class DexpressoClient is directly connected to web3 providers and Dexpresso backend.
It handles following functionalities:
    - creation and submition of limit orders
    - querying information and configurations of different markets/networks
    - querying orderbooks/latestfills/userfills/userorders/...
"""
from decimal import Decimal
from typing import List, Dict
from .Configs import DEXPRESSO_API_URL, GeneralNetwork
import requests


class GeneralClient:
    owner_address: str
    approve_gas: int
    average_block_time: Decimal
    access_token: str

    def __init__(self, network_obj: GeneralNetwork, owner_address: str, **kwargs):
        self.dexpresso_contract = network_obj.dexpresso_contract
        self.chain_id = network_obj.chain_id
        self.network = network_obj
        self.owner_address = owner_address

        # fill all available markets info
        res = self.get_markets_info()
        self.network.markets = {}
        for market in res['info']:
            if market:
                if len(market) > 0:
                    self.network.markets[market['display_name']] = market


    def authenticate(self, login_message: Dict):
        res = requests.post(f'{DEXPRESSO_API_URL}/login', json=login_message)
        results = res.json()
        self.access_token = results.get('access_token')
        return results

    def get_markets_info(self, markets: List[str] = None):
        params = {'network': self.network.name}
        if markets:
            params['markets'] = ','.join([market for market in markets])
        res = requests.get(f"{DEXPRESSO_API_URL}/markets/info", params=params)
        return res.json()

    def get_markets_config(self, markets: List[str] = None):
        params = {'network': self.network.name}
        if markets:
            params['markets'] = ','.join([market for market in markets])
        res = requests.get(f"{DEXPRESSO_API_URL}/markets/config", params=params)
        return res.json()

    def get_markets_stats(self, markets: List[str] = None):
        params = {'network': self.network.name}
        if markets:
            params['markets'] = ','.join([market for market in markets])
        res = requests.get(f"{DEXPRESSO_API_URL}/markets/stats", params=params)
        return res.json()

    def get_order_book(self, market: str, side: str = None, page: int = None, per_page: int = None):
        params = {
            'network': self.network.name,
            'market': market,
        }
        if side:
            params['side'] = 'b' if side in ['b', 'buy'] else 's'
        if page:
            params['page'] = page
        if per_page:
            params['per_page'] = per_page
        res = requests.get(f"{DEXPRESSO_API_URL}/orders", params=params)
        return res.json()

    def get_all_user_orders(self, market: str = None, start_time: str = None, end_time: str = None, page: int = None,
                            per_page: int = None):
        params = {}
        if market:
            params['market'] = market
        if start_time:
            params['start_time'] = start_time
        if end_time:
            params['end_time'] = end_time
        if page:
            params['page'] = page
        if per_page:
            params['per_page'] = per_page
        res = requests.get(f"{DEXPRESSO_API_URL}/user/orders", params=params)
        return res.json()

    def get_user_order(self, order_id: int):
        params = {'id': order_id}
        res = requests.get(f"{DEXPRESSO_API_URL}/user/order", params=params)
        return res.json()

    def submit_order(self, signed_order: Dict):
        res = requests.post(f"{DEXPRESSO_API_URL}/user/order", json=signed_order)
        return res.json()

    def cancel_all_user_orders(self, side: str = None, market: str = None):
        params = {}
        if market:
            params['market'] = market
        if side:
            params['side'] = 'b' if side in ['b', 'buy'] else 's'
        headers = {'Authorization': f'Bearer {self.access_token}'}
        res = requests.delete(f"{DEXPRESSO_API_URL}/user/orders", json=params)
        return res.json()

    def cancel_user_order(self, order_id: int):
        params = {'id': order_id}
        headers = {'Authorization': f'Bearer {self.access_token}'}
        res = requests.delete(f"{DEXPRESSO_API_URL}/user/order", json=params, headers=headers)
        return res.json()

    def get_latest_fills(self, market: str, page: int = None, per_page: int = None):
        params = {
            'network': self.network.name,
            'market': market,
        }
        if page:
            params['page'] = page
        if per_page:
            params['per_page'] = per_page
        res = requests.get(f"{DEXPRESSO_API_URL}/fills", params=params)
        return res.json()

    def get_user_fills(self, market: str = None):
        params = {}
        if market:
            params['market'] = market
        headers = {'Authorization': f'Bearer {self.access_token}'}
        res = requests.get(f"{DEXPRESSO_API_URL}/user/fills", params=params, headers=headers)
        return res.json()

