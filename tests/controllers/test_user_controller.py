import pytest
from brownie import web3, reverts


def test_usercontroller_deploy(user_controller):
    """
    Test if the contract is correctly deployed.
    """
    assert user_controller.get() == 5


def test_usercontroller_set(accounts, user_controller):
    """
    Test if the storage variable can be changed.
    """
    user_controller.set(20, {'from': accounts[0]})
    assert user_controller.get() == 20


def test_usercontroller_register(accounts, user_model, user_controller):
    """
    Test if user can register.
    """
    name = "alice"
    email = "alice@utexas.edu"
    user_controller.register(name, email, {'from': accounts[0]})

    response = user_model.getUser(accounts[0])
    expected = (accounts[0].address, name, email, False, False, False, web3.eth.get_block('latest').timestamp)
    assert response == expected


def test_usercontroller_registermultipletimes(accounts, user_model, user_controller):
    """
    Test if user can not register multiple times.
    """
    name = "alice"
    email = "alice@utexas.edu"
    user_controller.register(name, email, {'from': accounts[0]})

    with reverts():
        user_controller.register(name, email, {'from': accounts[0]})
        user_controller.register(name, email, {'from': accounts[0]})
    pass


def test_usercontroller_login(accounts, user_controller):
    """
    Test if login returns proper user.
    """
    name = "alice"
    email = "alice@utexas.edu"
    user_controller.register(name, email, {'from': accounts[0]})

    response = user_controller.login({'from': accounts[0]})
    expected = (accounts[0].address, name, email, False, False, False, web3.eth.get_block('latest').timestamp)
    assert response == expected


def test_usercontroller_remove(accounts, user_model, user_controller):
    """
    Test if user can delete his account.
    """
    user_controller.register("alice", "alice@utexas.edu", {'from': accounts[0]})
    user_controller.remove({'from': accounts[0]})

    response = user_model.getUser(accounts[0])
    expected = ("0x0000000000000000000000000000000000000000", "", "", False, False, False, 0)
    assert response == expected


@pytest.mark.skip(reason="update to admin acct")
def test_usercontroller_action(accounts, user_controller):
    """
    Test if admin can perform actions.
    """
    name = "alice"
    email = "alice@utexas.edu"
    user_controller.register(name, email, {'from': accounts[0]})
    user_controller.register("admin", "admin@utexas.edu", {'from': accounts[1]})

    user_controller.action(accounts[0], 0, {'from': accounts[1]})
    user_controller.action(accounts[0], 1, {'from': accounts[1]})
    user_controller.action(accounts[0], 2, {'from': accounts[1]})
    user_controller.action(accounts[0], 3, {'from': accounts[1]})
    pass


