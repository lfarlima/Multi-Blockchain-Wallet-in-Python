# Multi-Blockchain Wallet in Python
 Send transcations with ETH and BTC

# Multi-Blockchain Wallet in Python

## Background

Your new startup is focusing on building a portfolio management system that supports not only traditional assets
like gold, silver, stocks, etc, but crypto-assets as well! The problem is, there are so many coins out there! It's
a good thing you understand how HD wallets work, since you'll need to build out a system that can create them.

You're in a race to get to the market. There aren't as many tools available in Python for this sort of thing, yet.
Thankfully, you've found a command line tool, `hd-wallet-derive` that supports not only BIP32, BIP39, and BIP44, but
also supports non-standard derivation paths for the most popular wallets out there today! However, you need to integrate
the script into your backend with your dear old friend, Python.

Once you've integrated this "universal" wallet, you can begin to manage billions of addresses across 300+ coins, giving
you a serious edge against the competition.

In this assignment, however, you will only need to get 2 coins working: Ethereum and Bitcoin Testnet.
Ethereum keys are the same format on any network, so the Ethereum keys should work with your custom networks or testnets.



## Instructions

### 1. Generate a Mnemonic

- Generate a **new** 12 word mnemonic using `hd-wallet-derive` or by using [this tool](https://iancoleman.io/bip39/).

- Set this mnemonic as an environment variable by storing it a an `.env` file and importing it into your `wallet.py`.

### 2. Derive the wallet keys

- Create a function called `derive_wallets` that does the following:

  - Use the `subprocess` library to create a shell command that calls the `./derive` script from Python. Make sure to properly wait for the process. **Windows Users** may need to prepend the `php` command in front of `./derive` like so: `php ./derive`.

  - The following flags must be passed into the shell command as variables:
    - Mnemonic (`--mnemonic`) must be set from an environment variable, or default to a test mnemonic
    - Coin (`--coin`)
    - Numderive (`--numderive`) to set number of child keys generated
    - Format (`--format=json`) to parse the output into a JSON object using `json.loads(output)`

- Create a dictionary object called `coins` that uses the `derive_wallets` function to derive `ETH` and `BTCTEST` wallets.

- When done properly, the final object should look something like this (there are only 3 children each in this image):

  ![wallet-object](Images/wallet-object.png)

- You should now be able to select child accounts (and thus, private keys) by accessing items in the `coins` dictionary like so: `coins[COINTYPE][INDEX]['privkey']`.

### 3. Linking the transaction signing libraries

- Use `bit` and `web3.py` to leverage the keys stored in the `coins` object by creating three more functions:

  - `priv_key_to_account`:
  
    - This function will convert the `privkey` string in a child key to an account object that `bit` or `web3.py` can use to transact.
    - This function needs the following parameters:

      - `coin` -- the coin type (defined in `constants.py`).
      - `priv_key` -- the `privkey` string will be passed through here.

    - You will need to check the coin type, then return one of the following functions based on the library:

      - For `ETH`, return `Account.privateKeyToAccount(priv_key)`
          - This function returns an account object from the private key string. You can read more about this object [here](https://web3js.readthedocs.io/en/v1.2.0/web3-eth-accounts.html#privatekeytoaccount).
      - For `BTCTEST`, return `PrivateKeyTestnet(priv_key)`
          - This is a function from the `bit` libarary that converts the private key string into a WIF (Wallet Import Format) object. WIF is a special format bitcoin uses to designate the types of keys it generates. 
          - You can read more about this function [here](https://ofek.dev/bit/dev/api.html).

  - `create_tx`: 
    - This function will create the raw, unsigned transaction that contains all metadata needed to transact.
    - This function needs the following parameters:

      - `coin` -- the coin type (defined in `constants.py`).
      - `account` -- the account object from `priv_key_to_account`.
      - `to` -- the recipient address.
      - `amount` -- the amount of the coin to send.

    - You will need to check the coin type, then return one of the following functions based on the library:

      - For `ETH`, return an object containing `to`, `from`, `value`, `gas`, `gasPrice`, `nonce`, and `chainID`.
        Make sure to calculate all of these values properly using `web3.py`!
      - For `BTCTEST`, return `PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])`

- `send_tx`:
  - This function will call `create_tx`, sign the transaction, then send it to the designated network.
  - This function needs the following parameters:

    - `coin` -- the coin type (defined in `constants.py`).
    - `account` -- the account object from `priv_key_to_account`.
    - `to` -- the recipient address.
    - `amount` -- the amount of the coin to send.

  - You may notice these are the exact same parameters as `create_tx`. `send_tx` will call `create_tx`, so it needs all of this information available.

  - You will need to check the coin, then create a `raw_tx` object by calling `create_tx`. Then, you will need to sign the `raw_tx` using `bit` or `web3.py` (hint: the account objects have a sign transaction function within).

  - Once you've signed the transaction, you will need to send it to the designated blockchain network.

    - For `ETH`, return `w3.eth.sendRawTransaction(signed.rawTransaction)`
    - For `BTCTEST`, return `NetworkAPI.broadcast_tx_testnet(signed)`

### 4. Send some transactions!

- Now, you should be able to fund these wallets using testnet faucets. 
- Open up a new terminal window inside of `wallet`.
- Then run the command `python` to open the Python shell. 
- Within the Python shell, run the command `from wallet import *`. This will allow you to access the functions in `wallet.py` interactively.
- You'll need to set the account with  `priv_key_to_account` and use `send_tx` to send transactions.

  - **Bitcoin Testnet transaction**

    - Fund a `BTCTEST` address using [this testnet faucet](https://testnet-faucet.mempool.co/).

    - Use a [block explorer](https://tbtc.bitaps.com/) to watch transactions on the address.

    - Send a transaction to another testnet address (either one of your own, or the faucet's).

    - Screenshot the confirmation of the transaction like so:

      ![btc-test](Images/btc-test.png)

  - **Local PoA Ethereum transaction**

    - Add one of the `ETH` addresses to the pre-allocated accounts in your `networkname.json`.

    - Delete the `geth` folder in each node, then re-initialize using `geth --datadir nodeX init networkname.json`.
      This will create a new chain, and will pre-fund the new account.

    - [Add the following middleware](https://web3py.readthedocs.io/en/stable/middleware.html#geth-style-proof-of-authority)
      to `web3.py` to support the PoA algorithm:

      ```
      from web3.middleware import geth_poa_middleware

      w3.middleware_onion.inject(geth_poa_middleware, layer=0)
      ```

    - Due to a bug in `web3.py`, you will need to send a transaction or two with MyCrypto first, since the
      `w3.eth.generateGasPrice()` function does not work with an empty chain. You can use one of the `ETH` address `privkey`,
      or one of the `node` keystore files.

    - Send a transaction from the pre-funded address within the wallet to another, then copy the `txid` into
      MyCrypto's TX Status, and screenshot the successful transaction like so:

      ![eth-test](Images/eth-test.png)


