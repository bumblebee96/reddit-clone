
def test_user_controller_deploy(user_controller):
    """
    Test if the contract is correctly deployed.
    """
    assert user_controller.get() == 5


def test_user_controller_set(accounts, user_controller):
    """
    Test if the storage variable can be changed.
    """
    user_controller.set(20, {'from': accounts[0]})
    assert user_controller.get() == 20

    #set
    #get
    #update
    #delete
