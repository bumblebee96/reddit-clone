from brownie import web3


def test_postcontroller_deploy(post_controller):
    """
    Test if the contract is correctly deployed.
    """
    assert post_controller.get() == 5


def test_postcontroller_set(accounts, post_controller):
    """
    Test if the storage variable can be changed.
    """
    post_controller.set(20, {'from': accounts[0]})
    assert post_controller.get() == 20


def test_postcontroller_checkuser(accounts, user_controller, post_controller):
    """
    Test if user can post.
    """
    user_controller.register("alice", "alice@utexas.edu", {'from': accounts[0]})
    user_can_post = post_controller.checkIfUserExistsAndIsNotBanned({'from': accounts[0]})
    assert user_can_post == True


def test_postcontroller_getnextposts(accounts, user_controller, post_controller):
    """
    Test if the storage variable can be changed.
    """
    title = "title"
    body = "very cool post"
    link = "http://www.something.com"
    user_controller.register("alice", "alice@utexas.edu", {'from': accounts[0]})
    post_controller.submitNewPost(title, body, link, {'from': accounts[0]})

    response = post_controller.getNextPosts({'from': accounts[0]})
    expected_empty = [(0, "0x0000000000000000000000000000000000000000", "", "", "", 0, 0) for i in range(10)]
    exp_element = (0, accounts[0].address, title, body, link, web3.eth.get_block('latest').timestamp, 0)
    expected_empty[0] = exp_element
    assert response.return_value == tuple(expected_empty)


def test_postcontroller_submitnewpost(accounts, post_model, user_controller, post_controller):
    """
    Test if controller can write to model.
    """
    title = "title"
    body = "very cool post"
    link = "http://www.something.com"
    user_controller.register("alice", "alice@utexas.edu", {'from': accounts[0]})
    post_controller.submitNewPost(title, body, link, {'from': accounts[0]})

    response = post_model.getPost(0, {'from': accounts[0]})
    expected = (0, accounts[0].address, title, body, link, web3.eth.get_block('latest').timestamp, 0)
    assert response == expected


def test_postcontroller_deletepost(accounts, post_model, user_controller, post_controller):
    """
    Test if controller can delete from model.
    """
    title = "title"
    body = "very cool post"
    link = "http://www.something.com"
    user_controller.register("alice", "alice@utexas.edu", {'from': accounts[0]})
    post_controller.submitNewPost(title, body, link, {'from': accounts[0]})
    post_controller.deletePost(0, {'from': accounts[0]})

    assert post_model.posts_index() == 0


