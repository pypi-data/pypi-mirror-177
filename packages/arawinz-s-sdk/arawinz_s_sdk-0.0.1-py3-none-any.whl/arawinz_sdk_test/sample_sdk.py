import requests


def createWallet():
    Headers = { "tkn" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJrZXkiOiJIZWxsbyBmcm9tIFB1bGFyaXMifQ.jG9p7WQyIW581g_cAph4pQ0KbG6mPjl9QZsFgmoIyzY" }
    url = "https://blockchain.nowigence.ai/create_wallet"
    data = requests.get(url, headers=Headers)
    data = data.json()
    return data

def createWalletNew():
    Headers = { "tkn" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJrZXkiOiJIZWxsbyBmcm9tIFB1bGFyaXMifQ.jG9p7WQyIW581g_cAph4pQ0KbG6mPjl9QZsFgmoIyzY" }
    url = "https://blockchain.nowigence.ai/create_wallet"
    data = requests.get(url, headers=Headers)
    data = data.json()
    return data

# data = getData()

# print(data)