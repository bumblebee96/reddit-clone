import pytest
from brownie import web3


def test_commentmodel_deploy(comment_model):
    """
    Test if the contract is correctly deployed.
    """
    assert comment_model.get() == 5


def test_commentmodel_set(accounts, comment_model):
    """
    Test if the storage variable can be changed.
    """
    comment_model.set(20, {'from': accounts[0]})
    assert comment_model.get() == 20


def test_commentmodel_addcomment(accounts, comment_model):
    """
    Test if we can add a comment.
    """
    post_index = 0
    body = "very cool comment"
    comment_model.addComment(post_index, body, {'from': accounts[0]})
    pass


def test_commentmodel_removecomment(accounts, comment_model):
    """
    Test if we can remove a comment.
    """
    post_index = 0
    body = "very cool comment"
    comment_model.addComment(post_index, body, {'from': accounts[0]})
    comment_model.removeComment(post_index, 0, {'from': accounts[0]})
    pass


def test_commentmodel_getcomment(accounts, comment_model):
    """
    Test if we can retrive a comment.
    """
    post_index = 0
    body = "very cool comment"
    comment_model.addComment(post_index, body, {'from': accounts[0]})

    response = comment_model.getComment(post_index, 0, {'from': accounts[0]})
    expected = (post_index, 0, accounts[0].address, body, web3.eth.get_block('latest').timestamp, 0)
    assert response == expected


@pytest.mark.skip(reason="each comment has a different timestamp, makes it hard to test consistently")
def test_commentmodel_getallcomments(accounts, comment_model):
    """
    Test if we can retrive many comments.
    """
    post_index = 0
    body = "very cool comment"

    for i in range(13):
        comment_model.addComment(post_index, body, {'from': accounts[0]})
        pass

    response = comment_model.getAllComments(post_index, 0, {'from': accounts[0]})
    expected = [(post_index, i, accounts[0].address, body, web3.eth.get_block('latest').timestamp, 0) for i in range(10)]
    assert response == tuple(expected)


#TODO: add update function

