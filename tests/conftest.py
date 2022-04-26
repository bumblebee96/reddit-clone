import pytest


@pytest.fixture(autouse=True)
def setup(fn_isolation):
    """
    Isolation setup fixture.
    This ensures that each test runs against the same base environment.
    """
    pass


@pytest.fixture(scope="module")
def vyper_storage(accounts, VyperStorage):
    """
    Yield a `Contract` object for the VyperStorage contract.
    """
    yield accounts[0].deploy(VyperStorage)


@pytest.fixture(scope="module")
def solidity_storage(accounts, SolidityStorage):
    """
    Yield a `Contract` object for the SolidityStorage contract.
    """
    yield accounts[0].deploy(SolidityStorage)



@pytest.fixture(scope="module")
def user_model(accounts, UserModel):
    """
    Yield a `Contract` object for the UserModel contract.
    """
    yield accounts[0].deploy(UserModel)


@pytest.fixture(scope="module")
def comment_model(accounts, CommentModel):
    """
    Yield a `Contract` object for the CommentModel contract.
    """
    yield accounts[0].deploy(CommentModel)


@pytest.fixture(scope="module")
def post_model(accounts, PostModel):
    """
    Yield a `Contract` object for the PostModel contract.
    """
    yield accounts[0].deploy(PostModel)


@pytest.fixture(scope="module")
def comment_controller(accounts, comment_model, user_model, CommentController):
    """
    Yield a `Contract` object for the CommentController contract.
    """
    yield accounts[0].deploy(CommentController, comment_model, user_model)


@pytest.fixture(scope="module")
def post_controller(accounts, comment_model, post_model, user_model, PostController):
    """
    Yield a `Contract` object for the PostController contract.
    """
    yield accounts[0].deploy(PostController, comment_model, post_model, user_model)


@pytest.fixture(scope="module")
def user_controller(accounts, post_model, user_model, UserController):
    """
    Yield a `Contract` object for the UserController contract.
    """
    yield accounts[0].deploy(UserController, post_model, user_model)
