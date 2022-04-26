# Reddit Clone

Reddit Clone MVC app

## To run the project

Go to each of the directories and install the dependencies:

`cd client`

`npm install`

Run the backend:

`ganache-cli --chain.vmErrorsOnRPCResponse true --server.port 8545 --miner.blockGasLimit 12000000 --wallet.totalAccounts 10 --hardfork istanbul --wallet.mnemonic brownie`

`brownie run scripts/deploy_controllers.py`

Run the frontend:

`npm start`


