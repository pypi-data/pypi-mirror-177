"""
-------------------------------------
-- Dexpresso.protocol: LazyClient.py --
-------------------------------------
Class DexpressoLazyClient is directly connected to web3 providers and Dexpresso backend.
It combines all the functionalities from Client.py and OfflineSigner.py:
    - creation, sign and submission of limit orders
    - querying information and configurations of different markets/networks
    - querying orderbooks/latestfills/userfills/userorders/...
"""
import asyncio
import json
from decimal import Decimal
from fractions import Fraction
from typing import List
import requests
from eth_account import Account
from eth_account.messages import encode_defunct
from eth_keys import keys
from web3 import Web3, HTTPProvider
from zksync_sdk import ZkSyncLibrary, network, ZkSyncProviderV01, HttpJsonRPCTransport, EthereumSignerWeb3, ZkSync, \
    EthereumProvider, ZkSyncSigner, Wallet
from zksync_sdk.types import ChainId, RatioType

from .Configs import ZkSyncOneNetwork, DEXPRESSO_API_URL
from .GeneralClient import GeneralClient


class ZkSyncOneEasyClient(GeneralClient):
    privkey: str
    pubkey: str
    owner_address: str
    w3: Web3
    network: ZkSyncOneNetwork
    _latest_uuid: str
    access_token: str

    def __init__(self, network_obj: ZkSyncOneNetwork, privkey: str):
        self.privkey = privkey
        self.pubkey = keys.PrivateKey(bytes.fromhex(privkey)).public_key.to_bytes().hex()
        owner_address = Account.from_key(privkey).address
        super().__init__(network_obj, owner_address)

        library = ZkSyncLibrary()
        zksync_network = network.Network(
            zksync_url=network_obj.zk_provider_url, chain_id=ChainId(self.network.chain_id)
        )
        provider = ZkSyncProviderV01(
            provider=HttpJsonRPCTransport(network=zksync_network)
        )
        account = Account.from_key(privkey)
        ethereum_signer = EthereumSignerWeb3(account=account)
        contracts = asyncio.run(provider.get_contract_address())
        self.w3 = Web3(HTTPProvider(network_obj.provider_url))
        zksync = ZkSync(
            account=account, web3=self.w3, zksync_contract_address=contracts.main_contract
        )
        ethereum_provider = EthereumProvider(self.w3, zksync)
        signer = ZkSyncSigner.from_account(account, library, zksync_network.chain_id)
        self.wallet = Wallet(
            ethereum_provider=ethereum_provider,
            zk_signer=signer,
            eth_signer=ethereum_signer,
            provider=provider,
        )

        # Get user id
        self.user_id = asyncio.run(self.wallet.get_account_id())

    def sign_message(self, message: str):
        signed_message = self.w3.eth.account.sign_message(
            encode_defunct(text=message), private_key=self.privkey
        )
        return str(signed_message.signature.hex())

    def authenticate(self, user_data=False, uuid=None):
        login_body = {
            'network': self.network.name,
            'address': self.owner_address,
            'signature': self.sign_message("Login to Dexpresso"),
            'user_data': user_data,
            'uuid': uuid or "",
        }
        res = requests.post(f'{DEXPRESSO_API_URL}/login', json=login_body)
        results = res.json()
        self.access_token = results.get('access_token')
        return results

    def create_and_submit_order(self, market: str, side: str, price: Decimal, amount: Decimal, expiration: int, fee: Decimal):
        if side not in ['b', 's', 'buy', 'sell']:
            raise "Given side is not valid!\n" \
                  "Available options: 1) 'buy' or 'b',  2) 's' or 'sell'"
        if market not in self.network.markets:
            raise f"Given market is not available in this network!\n" \
                  f"Available options: {self.network.markets.keys()}"
        
        market_pair = market
        
        # start zksync zone
        src = market_pair.split("-")[0]
        dst = market_pair.split("-")[1]

        if side in ['sell', 's']:
            final_price = Decimal(price * (1 - fee))
            ratio = Fraction(1, Fraction.from_decimal(final_price))
            zksync_order = asyncio.run(self.wallet.get_order(
                src, dst, ratio, RatioType.token, Decimal("0"), valid_until=2000000000
            ))
            packedSellQuantity = self.wallet.tokens.find_by_symbol(src).from_decimal(
                amount
            )
            order_side = 's'

        else:
            final_price = Decimal(price * (1 + fee)).__round__(10)
            ratio = Fraction.from_decimal(final_price)
            zksync_order = asyncio.run(self.wallet.get_order(
                dst, src, ratio, RatioType.token, Decimal("0"), valid_until=2000000000
            ))
            packedSellQuantity = self.wallet.tokens.find_by_symbol(dst).from_decimal(
                amount * final_price
            )
            order_side = 'l'

        order = {
            "accountId": zksync_order.account_id,
            "recipient": zksync_order.recipient,
            "nonce": zksync_order.nonce,
            "amount": str(zksync_order.amount),
            "tokenSell": zksync_order.token_sell.id,
            "tokenBuy": zksync_order.token_buy.id,
            "validFrom": zksync_order.valid_from,
            "validUntil": zksync_order.valid_until,
            "ratio": [
                str(zksync_order.ratio.numerator),
                str(zksync_order.ratio.denominator),
            ],
            "signature": {
                "pubKey": zksync_order.signature.public_key,
                "signature": zksync_order.signature.signature,
            },
            "ethSignature": {
                "type": zksync_order.eth_signature.sig_type.value,
                "signature": zksync_order.eth_signature.signature,
            },
        }
        final_dict = {
            'tx': order,
            "market": market,
            "amount": str(packedSellQuantity),
            "price": str(float(price)),
            "type": order_side
        }
        # end zksync zone
        header = {'Authorization': f'Bearer {self.access_token}'}
        res = requests.post(f"{DEXPRESSO_API_URL}/user/order", json=final_dict, headers=header)
        return res.json()
