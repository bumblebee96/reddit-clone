// SPDX-License-Identifier: GPL-3.0
pragma solidity 0.8.0;

import "../models/CommentModel.sol";
import "../models/PostModel.sol";
import "../models/UserModel.sol";

contract PostController
{
  CommentModel cm;
  PostModel pm;
  UserModel um;
  uint cur_post_page;

  constructor()
  {
    //TODO: set address of post model contract in config
    cm = CommentModel(msg.sender);
    pm = PostModel(msg.sender);
    um = UserModel(msg.sender);
    cur_post_page = 0;
  }

  function checkIfUserExistsAndIsNotBanned() public view returns (bool)
  {
    bool user_already_exists = um.doesUserExist(msg.sender);
    require(user_already_exists, "There is no user with that username");

    UserStruct.User memory user = um.getUser(msg.sender);
    return user.banned;
  }

  function getNextPosts() public returns(PostStruct.Post[POST_PAGE_SIZE] memory)
  {
    uint post_count = pm.posts_index();
    uint next = POST_PAGE_SIZE * (cur_post_page + 1);

    if(next < post_count)
    {
      cur_post_page++;
    }
    else
    {
      cur_post_page = 0;
    }

    return pm.getAllPosts(cur_post_page);
  }

  function submitNewPost(string memory title, string memory text, string memory link) public
  {
    pm.addPost(title, text, link);
  }

  function getSinglePostAndComments(uint post_id) public
  returns(PostStruct.Post memory, CommentStruct.Comment[COMM_PAGE_SIZE] memory)
  {
    PostStruct.Post memory post = pm.getPost(post_id);
    CommentStruct.Comment[COMM_PAGE_SIZE] memory comments = cm.getAllComments(post_id, 0);

    return (post, comments);
  }

  function deletePost(uint post_id) public
  {
    bool user_already_exists = um.doesUserExist(msg.sender);
    require(user_already_exists, "There is no user with that username");

    UserStruct.User memory user = um.getUser(msg.sender);
    PostStruct.Post memory post = pm.getPost(post_id);
    require(user.isAdmin || user.username == post.username, "You are not authorized to perform this action!");

    pm.removePost(post_id);
    //TODO: remove comments
  }

  //postController.getAllPostsByUser = async (req, res) => {

  uint256 storedData = 5;

  function set(uint256 _x) public
  {
    storedData = _x;
  }

  function get() public view returns (uint256)
  {
    return storedData;
  }
}
