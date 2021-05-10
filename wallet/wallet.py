# # Import dependencies
import os
import subprocess
import json
# from dotenv import load_dotenv
# from bit import wif_to_key

# Load and set environment variables
# load_dotenv()
# mnemonic=os.getenv("mnemonic")

# from bit import PrivateKeyTestnet
# from bit.network import NetworkAPI
# from web3 import Web3, middleware, Account
# from web3.gas_strategies.time_based import medium_gas_price_strategy
# from web3.middleware import geth_poa_middleware
# # connect Web3
# w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
# # enable PoA middleware
# w3.middleware_onion.inject(geth_poa_middleware, layer=0)
# # set gas price strategy to built-in "medium" algorithm (est ~5min per tx)
# # see https://web3py.readthedocs.io/en/stable/gas_price.html?highlight=gas
# # see https://ethgasstation.info/ API for a more accurate strategy
# w3.eth.setGasPriceStrategy(medium_gas_price_strategy)

# Import constants.py and necessary functions from bit and web3
# from constants import *

# BTC = 'btc'
# ETH = 'eth'
# BTCTEST = 'btc-test'

# # mnemonic = 'above pelican steel canoe grocery harbor access smart oak approve hen measure toilet salad author'
# fxcoin = ETH

# Create a function called `derive_wallets`
# def derive_wallets(mnemonic=mnemonic, fxcoin=ETH, depth=3):
command = './derive -g --mnemonic="above pelican steel canoe grocery harbor access smart oak approve hen measure toilet salad author" --cols=path,address,privkey,pubkey --coin=ETH --format=json' # --numderive={depth}'

p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()
p_status = p.wait()

keys = json.loads(output)
print (keys)
    # return keys
# Create a dictionary object called coins to store the output from `derive_wallets`.
# coins = derive_wallets(fxcoin=ETH)
# print(coins)

# # Create a function called `priv_key_to_account` that converts privkey strings to account objects.
# def priv_key_to_account(# YOUR CODE HERE):
#     # YOUR CODE HERE

# # Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
# def create_tx(# YOUR CODE HERE):
#     # YOUR CODE HERE

# # Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
# def send_tx(# YOUR CODE HERE):
#     # YOUR CODE HERE

