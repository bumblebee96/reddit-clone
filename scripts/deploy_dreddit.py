from scripts.helpful_scripts import get_account
from scripts.helpful_scripts import deploy_models, deploy_controllers

from brownie  import UserController, PostController, CommentController


def first_post():
    cc = CommentController[-1]
    pc = PostController[-1]
    uc = UserController[-1]

    print("Register")
    alice = get_account(0)
    bob = get_account(1)
    a = uc.register("alice", "alice@utexas.edu", {"from": alice})
    b = uc.register("bob", "bob@utexas.edu", {"from": bob})

    print("Post")
    title = "[HELP] does anyone understand the assignment?"
    body = "i need help on ee306 problem set"
    link = "http://users.ece.utexas.edu/~patt/15f.306/ProblemSets/PS3/ps3.html"
    pc.submitNewPost(title, body, link, {"from": bob})

    print("Comment")
    text = "there is a study group meeting at PCL if you want to join"
    cc.submitComment(0, text, {"from": alice})
    pass


def view_out():
    cc = CommentController[-1]
    pc = PostController[-1]

    posts = pc.getNextPosts()
    print("all posts:")
    print(posts.return_value)

    comments = cc.getNextComments(0)
    print("all comments:")
    print(comments.return_value)
    pass


def main():
    deploy_models()
    deploy_controllers()

    print("First interaction:")
    first_post()
    print("Output:")
    view_out()
