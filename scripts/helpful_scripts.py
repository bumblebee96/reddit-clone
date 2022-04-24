from brownie  import UserModel, PostModel, CommentModel
from brownie  import UserController, PostController, CommentController

from brownie import accounts, network, config, Contract

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


def get_account(index=None, id=None):
    # accounts[0]
    # accounts.add("env")
    # accounts.load("id")
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or
        network.show_active() in FORKED_LOCAL_ENVIRONMENTS):
        return accounts[0]

    return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {
    "comment_model": CommentModel,
    "post_model": PostModel,
    "user_model": UserModel,
}


def get_contract(contract_name):
    """This function will grab the contract addresses from the brownie config
    if defined, otherwise, it will deploy a mock version of that contract, and
    return that mock contract.

        Args:
            contract_name (string)

        Returns:
            brownie.network.contract.ProjectContract: The most recently deployed
            version of this contract.
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_models()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)

    return contract


def deploy_models():
    account = get_account()

    CommentModel.deploy({"from": account})
    PostModel.deploy({"from": account})
    UserModel.deploy({"from": account})

    print("Models Deployed!")


def deploy_controllers():
    account = get_account()
    cm = get_contract("comment_model").address
    pm = get_contract("post_model").address
    um = get_contract("user_model").address

    CommentController.deploy(cm, um, {"from": account})
    PostController.deploy(cm, pm, um, {"from": account})
    UserController.deploy(pm, um, {"from": account})

    print("Controllers Deployed!")


