// SPDX-License-Identifier: GPL-3.0
pragma solidity 0.8.0;

import "OpenZeppelin/openzeppelin-contracts@4.5.0/contracts/utils/math/Math.sol";

uint constant COMM_PAGE_SIZE = 10;

library CommentStruct
{
  struct Comment
  {
    uint post_id;
    uint comment_id;
    address username;
    string comment;
    uint date_created;
    uint score;
    //upvotedby: [ { type: mongoose.Schema.ObjectId, ref: 'User' } ],
    //downvotedby: [ { type: mongoose.Schema.ObjectId, ref: 'User' } ]
  }
}

contract CommentModel
{
  //post_id => comments
  mapping(uint => CommentStruct.Comment[]) comments;

  function addComment(uint post_id, string memory comment_body) public
  {
    uint score = 0;
    uint date_created = block.timestamp;
    CommentStruct.Comment memory element = CommentStruct.Comment(post_id, comments[post_id].length, tx.origin, comment_body, date_created, score);

    comments[post_id].push(element);
  }
  
  function removeComment(uint post_id, uint comment_id) public
  {
    uint len = comments[post_id].length;
    require(comment_id < len, "need valid comment id");

    comments[post_id][comment_id] = comments[post_id][len - 1];
    comments[post_id].pop();
  }

  function getComment(uint post_id, uint comment_id) public view returns(CommentStruct.Comment memory)
  {
    uint len = comments[post_id].length;
    require(comment_id < len, "need valid comment id");

    return comments[post_id][comment_id];
  }

  function getAllComments(uint post_id, uint page) public view returns(CommentStruct.Comment[COMM_PAGE_SIZE] memory)
  {
    CommentStruct.Comment[COMM_PAGE_SIZE] memory ret_data;
    uint comments_len = comments[post_id].length;
    uint starting_index = page * COMM_PAGE_SIZE;
    uint last_index = Math.min(comments_len, starting_index + COMM_PAGE_SIZE);
    require(starting_index < comments_len, "need valid page number");

    for(uint i = starting_index; i < last_index; i++)
    {
      ret_data[i - starting_index] = comments[post_id][i];
    }

    return ret_data;
  }

  function getCommentCountByPost(uint post_id) public view returns(uint)
  {
    return comments[post_id].length;
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
