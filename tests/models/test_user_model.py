
def test_usermodel_deploy(user_model):
    """
    Test if the contract is correctly deployed.
    """
    assert user_model.get() == 5


def test_usermodel_set(accounts, user_model):
    """
    Test if the storage variable can be changed.
    """
    user_model.set(20, {'from': accounts[0]})
    assert user_model.get() == 20


def test_usermodel_adduser(accounts, user_model):
    """
    Test if user can be added.
    """
    user_model.addUser('enoc', 'enoc@gmail.com', {'from': accounts[0]})
    assert user_model.count() == 1


def test_usermodel_removeuser(accounts, user_model):
    """
    Test if user can be removed.
    """
    user_model.addUser('enoc', 'enoc@gmail.com', {'from': accounts[0]})
    user_model.removeUser({'from': accounts[0]})
    assert user_model.count() == 0


def test_usermodel_doesuserexist(accounts, user_model):
    """
    Test if user exists.
    """
    user_model.addUser('enoc', 'enoc@gmail.com', {'from': accounts[0]})
    assert user_model.doesUserExist(accounts[0], {'from': accounts[0]}) == True

    user_model.removeUser({'from': accounts[0]})
    assert user_model.doesUserExist(accounts[0], {'from': accounts[0]}) == False

    #set
    #get
    #update
    #delete
