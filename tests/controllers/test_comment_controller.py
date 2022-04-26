from brownie import web3


def test_commentcontroller_deploy(comment_controller):
    """
    Test if the contract is correctly deployed.
    """
    assert comment_controller.get() == 5


def test_commentcontroller_set(accounts, comment_controller):
    """
    Test if the storage variable can be changed.
    """
    comment_controller.set(20, {'from': accounts[0]})
    assert comment_controller.get() == 20


def test_commentcontroller_getnextcomments(accounts, user_controller, comment_controller):
    """
    Test if the storage variable can be changed.
    """
    text = "very cool comment"
    user_controller.register("alice", "alice@utexas.edu", {'from': accounts[0]})
    comment_controller.submitComment(0, text, {'from': accounts[0]})

    response = comment_controller.getNextComments(0, {'from': accounts[0]})
    expected_empty = [(0, 0, "0x0000000000000000000000000000000000000000", "", 0, 0) for i in range(10)]
    exp_element = (0, 0, accounts[0].address, text, web3.eth.get_block('latest').timestamp, 0)
    expected_empty[0] = exp_element
    assert response.return_value == tuple(expected_empty)


def test_commentcontroller_submitcomment(accounts, comment_model, user_controller, comment_controller):
    """
    Test if the storage variable can be changed.
    """
    text = "very cool comment"
    user_controller.register("alice", "alice@utexas.edu", {'from': accounts[0]})
    comment_controller.submitComment(0, text, {'from': accounts[0]})

    response = comment_model.getComment(0, 0, {'from': accounts[0]})
    expected = (0, 0, accounts[0].address, text, web3.eth.get_block('latest').timestamp, 0)
    assert response == expected


def test_commentcontroller_deletecomment(accounts, comment_model, user_controller, comment_controller):
    """
    Test if the storage variable can be changed.
    """
    text = "very cool comment"
    user_controller.register("alice", "alice@utexas.edu", {'from': accounts[0]})

    comment_controller.submitComment(0, text, {'from': accounts[0]})
    response = comment_model.getComment(0, 0, {'from': accounts[0]})
    expected = (0, 0, accounts[0].address, text, web3.eth.get_block('latest').timestamp, 0)
    assert response == expected

    comment_controller.deleteComment(0, 0, {'from': accounts[0]})
    assert comment_model.getCommentCountByPost(0) == 0


