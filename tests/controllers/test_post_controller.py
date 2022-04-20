
def test_post_controller_deploy(post_controller):
    """
    Test if the contract is correctly deployed.
    """
    assert post_controller.get() == 5


def test_post_controller_set(accounts, post_controller):
    """
    Test if the storage variable can be changed.
    """
    post_controller.set(20, {'from': accounts[0]})
    assert post_controller.get() == 20

    #set
    #get
    #update
    #delete
