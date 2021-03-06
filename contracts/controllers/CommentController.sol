// SPDX-License-Identifier: GPL-3.0
pragma solidity 0.8.0;

import "../models/CommentModel.sol";
import "../models/UserModel.sol";

contract CommentController
{
  CommentModel cm;
  UserModel um;
  uint cur_comm_page;
  uint prev_post_id;

  constructor(address comment_model_addr, address user_model_addr)
  {
    cm = CommentModel(comment_model_addr);
    um = UserModel(user_model_addr);
    cur_comm_page = 0;
    prev_post_id = 0;
  }

  function getNextComments(uint post_id) public returns(CommentStruct.Comment[COMM_PAGE_SIZE] memory)
  {
    if(prev_post_id != post_id)
    {
      prev_post_id = post_id;
      cur_comm_page = 0;
    }

    uint comm_count = cm.getCommentCountByPost(post_id);
    uint next = COMM_PAGE_SIZE * (cur_comm_page + 1);

    if(next < comm_count)
    {
      cur_comm_page++;
    }
    else
    {
      cur_comm_page = 0;
    }

    return cm.getAllComments(post_id, cur_comm_page);
  }

  function submitComment(uint post_id, string memory text) public
  {
    bool user_already_exists = um.doesUserExist(msg.sender);
    require(user_already_exists, "There is no user with that username");

    cm.addComment(post_id, text);
  }

  function deleteComment(uint post_id, uint comm_id) public
  {
    bool user_already_exists = um.doesUserExist(msg.sender);
    require(user_already_exists, "There is no user with that username");

    UserStruct.User memory user = um.getUser(msg.sender);
    CommentStruct.Comment memory comm = cm.getComment(post_id, comm_id);
    require(user.isAdmin || user.username == comm.username, "You are not authorized to perform this action!");

    cm.removeComment(post_id, comm_id);
  }

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
