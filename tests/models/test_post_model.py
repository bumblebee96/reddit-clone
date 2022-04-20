import pytest
from brownie import web3


def test_postmodel_deploy(post_model):
    """
    Test if the contract is correctly deployed.
    """
    assert post_model.get() == 5


def test_postmodel_set(accounts, post_model):
    """
    Test if the storage variable can be changed.
    """
    post_model.set(20, {'from': accounts[0]})
    assert post_model.get() == 20


def test_postmodel_addpost(accounts, post_model):
    """
    Test if we can add a post.
    """
    title = "title"
    body = "very cool post"
    link = "http://www.something.com"
    post_model.addPost(title, body, link, {'from': accounts[0]})
    assert post_model.posts_index() == 1


def test_postmodel_removepost(accounts, post_model):
    """
    Test if we can remove a post.
    """
    title = "title"
    body = "very cool post"
    link = "http://www.something.com"
    post_model.addPost(title, body, link, {'from': accounts[0]})
    post_model.removePost(0, {'from': accounts[0]})
    assert post_model.posts_index() == 0


def test_postmodel_getpost(accounts, post_model):
    """
    Test if we can retrive a post.
    """
    title = "title"
    body = "very cool post"
    link = "http://www.something.com"
    post_model.addPost(title, body, link, {'from': accounts[0]})

    response = post_model.getPost(0, {'from': accounts[0]})
    expected = (0, accounts[0].address, title, body, link, web3.eth.get_block('latest').timestamp, 0)
    assert response == expected


@pytest.mark.skip(reason="each comment has a different timestamp, makes it hard to test consistently")
def test_postmodel_getallposts(accounts, post_model):
    """
    Test if we can retrive many posts.
    """
    title = "title"
    body = "very cool post"
    link = "http://www.something.com"

    for i in range(13):
        post_model.addPost(title, body, link, {'from': accounts[0]})
        pass

    response = post_model.getAllPosts(0, {'from': accounts[0]})
    expected = [(i, accounts[0].address, title, body, link, web3.eth.get_block('latest').timestamp, 0) for i in range(10)]
    assert response == tuple(expected)


#TODO: add update function

