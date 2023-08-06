import requests

from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future import transaction
from algosdk.logic import get_application_address
from pytz import timezone

algod_address = "https://testnet-api.algonode.cloud"
algod_token = ""
algod_client = algod.AlgodClient(algod_token, algod_address)
params = algod_client.suggested_params()


class ArawinzSdk:
    def createWallet():
        private_key, address = account.generate_account()
        return {'wallet_address':address,'pass_phrase':mnemonic.from_private_key(private_key)}

# def createWallet():
#     Headers = { "tkn" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJrZXkiOiJIZWxsbyBmcm9tIFB1bGFyaXMifQ.jG9p7WQyIW581g_cAph4pQ0KbG6mPjl9QZsFgmoIyzY" }
#     url = "https://blockchain.nowigence.ai/create_wallet"
#     data = requests.get(url, headers=Headers)
#     data = data.json()
#     return data

# def createWalletNew():
#     Headers = { "tkn" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJrZXkiOiJIZWxsbyBmcm9tIFB1bGFyaXMifQ.jG9p7WQyIW581g_cAph4pQ0KbG6mPjl9QZsFgmoIyzY" }
#     url = "https://blockchain.nowigence.ai/create_wallet"
#     data = requests.get(url, headers=Headers)
#     data = data.json()
#     return data

# data = getData()

# print(data)