
def test_comment_controller_deploy(comment_controller):
    """
    Test if the contract is correctly deployed.
    """
    assert comment_controller.get() == 5


def test_comment_controller_set(accounts, comment_controller):
    """
    Test if the storage variable can be changed.
    """
    comment_controller.set(20, {'from': accounts[0]})
    assert comment_controller.get() == 20

    #set
    #get
    #update
    #delete
