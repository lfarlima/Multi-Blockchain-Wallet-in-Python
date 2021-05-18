import sys
import os
from bit.transaction import sign_tx
import pandas as pd
from coincurve import keys
from dotenv import load_dotenv
import subprocess
import json
from bit import wif_to_key

from bit import PrivateKeyTestnet
from bit.network import NetworkAPI
from web3 import Web3, middleware, Account
from web3.gas_strategies.time_based import medium_gas_price_strategy
from web3.middleware import geth_poa_middleware
from eth_account import Account
from getpass import getpass

import requests


# connect to Web3
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# set gas price strategy to built-in "medium" algorithm (est ~5min per tx)
# see https://web3py.readthedocs.io/en/stable/gas_price.html?highlight=gas
# see https://ethgasstation.info/ API for a more accurate strategy
w3.eth.setGasPriceStrategy(medium_gas_price_strategy)

# Load and set environment variables
load_dotenv()
mnemonic=os.getenv("mnemonic")

# Set constants
BTC = 'btc'
ETH = 'eth'
BTCTEST = 'btc-test'

# Create function to derive wallets:
def derive_wallets(mnemonic,coin,depth):
    command = './derive -g --mnemonic=mnemonic --cols=all --coin=ETH --numderive=3 --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status=p.wait()
    keys = json.loads(output)
    return keys

# Create a dictionary object called coins to store the output from `derive_wallets`.
coins = {ETH,BTC}
key = {}
for coin in coins:
    key[coin]=derive_wallets(mnemonic,coin,3)

# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
def priv_key_to_account(coin,priv_key):
    # print(coin)
    # print(priv_key)
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    elif coin == BTC:
        key = wif_to_key("")
        return key.PrivateKeyTestnet(priv_key)

print(key)



# Create a variable to hold keys
eth_owner = priv_key_to_account(ETH,key['eth'][0]['privkey'])
print(eth_owner)

# # Create a variable to hold coins
eth_recipient = key['eth'][2]['address']
eth_recipient_pubkey = key['eth'][2]['pubkey']
print(eth_recipient)


print(key['btc'])
print("*******")
print(key['eth'])

btc_owner = priv_key_to_account(BTC,key['btc'][2]['xprv']) # unable to get this to run without error
btc_recipient = key['btc'][2]['address']
btc_recipient_pubkey = key['btc'][2]['pubkey']

# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
def create_tx(coin, account, recipient, amount):
    if coin == ETH:
        gasEstimate = w3.eth.estimateGas(
            {"from": account, "to": recipient, "value": amount})
        return {
            "from": account,
            "to": recipient, 
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(w3.toChecksumAddress(account.address))}
    elif coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(btc_acc,[(recipient,amount,BTC)])

# # Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_tx(coin, account, recipient, amount):
    if coin == ETH:
        raw_tx = create_tx(coin, account, recipient,amount)
        signed_tx = account.sign_transaction(raw_tx)
        result = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print (result.hex())
        return result.hex()
    elif coin == BTCTEST:
        raw_tx = create_tx(coin, account, recipient,amount)
        signed_tx = account.bit(sign_tx(raw_tx))
        result = account.bit(send_tx(signed_tx))
        print (result.hex())
        return result.hex()

txHash = send_tx(ETH, eth_owner, eth_recipient, w3.toWei(12345,'ether')) 
print(txHash)

# txHash = send_tx(BTC, btc_owner, btc_recipient, w3.toWei(12345,'ether')) 
# print(txHash)