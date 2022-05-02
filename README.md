# Reddit Clone

Reddit MVC clone

## Installation
1. Create virtual env.
    ```bash
    python3 -m venv venv
    ```

2. Activate virtual env.
    ```bash
    source venv/bin/activate
    ```

3. Install required pip packages.
    ```bash
    pip install -r requirements.txt
    ```

4. Install required npm packages.
    ```bash
    cd ./client
    npm install
    ```


## Usage

1. Open the Brownie console. Starting the console launches a fresh [Ganache](https://www.trufflesuite.com/ganache) instance in the background.

    ```bash
    $ brownie console
    Brownie v1.18.1 - Python development framework for Ethereum

    DredditProject is the active project.
    Launching 'ganache-cli --chain.vmErrorsOnRPCResponse true --server.port 8545 --miner.blockGasLimit 12000000 --wallet.totalAccounts 10 --hardfork istanbul --wallet.mnemonic brownie'...
    Brownie environment is ready.
    ```

2. Run the [deployment script](scripts/deploy_controllers.py) to deploy the project's smart contracts.

    ```python
    >>> run("deploy_controllers")

    Running 'scripts/deploy_controllers.py::main'...
    Transaction sent: 0x70e557ef7885860dc3ee3b4e6f14622e4c6fe1dbe2cbeedffb849171c8a204b2
      Gas price: 0.0 gwei   Gas limit: 12000000   Nonce: 0
      CommentModel.constructor confirmed   Block: 1   Gas used: 744383 (6.20%)
      CommentModel deployed at: 0x3194cBDC3dbcd3E11a07892e7bA5c3394048Cc87

    Transaction sent: 0x3ba8f4b90e1658cb3e93fc3780935a5407f6729fa961c0a00fb738b4080c38e9
      Gas price: 0.0 gwei   Gas limit: 12000000   Nonce: 1
      PostModel.constructor confirmed   Block: 2   Gas used: 927789 (7.73%)
      PostModel deployed at: 0x602C71e4DAC47a042Ee7f46E0aee17F94A3bA0B6

    Transaction sent: 0x5d6679a75c34befe4625cd53c84ac9160e9abc9454c5c8511b1cedadae3a1099
      Gas price: 0.0 gwei   Gas limit: 12000000   Nonce: 2
      UserModel.constructor confirmed   Block: 3   Gas used: 648868 (5.41%)
      UserModel deployed at: 0xE7eD6747FaC5360f88a2EFC03E00d25789F69291

    Models Deployed!
    Transaction sent: 0x3a991cfb1a1b87a7ff2095fdf9d12ebc775f08a632ab0d23b6de34beb17efb6c
      Gas price: 0.0 gwei   Gas limit: 12000000   Nonce: 3
      CommentController.constructor confirmed   Block: 4   Gas used: 822718 (6.86%)
      CommentController deployed at: 0x6951b5Bd815043E3F842c1b026b0Fa888Cc2DD85

    Transaction sent: 0xb729de725122cc046f36663c9a77de0885dec58128d961ca715b2b8b068bb7f5
      Gas price: 0.0 gwei   Gas limit: 12000000   Nonce: 4
      PostController.constructor confirmed   Block: 5   Gas used: 1140029 (9.50%)
      PostController deployed at: 0xe0aA552A10d7EC8760Fc6c246D391E698a82dDf9

    Transaction sent: 0xb3957329177692986593b9334406a509e98c6f29d8d7660ea7588c11da220fb8
      Gas price: 0.0 gwei   Gas limit: 12000000   Nonce: 5
      UserController.constructor confirmed   Block: 6   Gas used: 815862 (6.80%)
      UserController deployed at: 0x6b4BDe1086912A6Cb24ce3dB43b3466e6c72AFd3

    Controllers Deployed!
    ```

3. While Brownie is still running, start the React app in a different terminal.

    The first time this app is used, the node modules have to be installed in /src.
    To do this, navigate to ./client and run

    ```bash
    # make sure to use a different terminal, not the brownie console
    npm install
    npm audit fix
    npm start
    ```

4. Connect Metamask to the local Ganache network. In the upper right corner, click the network dropdown menu. Select `Localhost 8545`:



5. Interact with the smart contracts using the web interface or via the Brownie console.

    ```python
    # get the newest user controller contract
    >>> uc = UserController[-1]

    # register a new user
    >>> alice = get_account(0)
    >>> uc.register("alice", "alice@utexas.edu", {"from": alice})
    ```

    Any changes to the contracts from the console should show on the website after a refresh, and vice versa.

## Further Possibilities

### Testing

To run the test suite:

```bash
brownie test
```

