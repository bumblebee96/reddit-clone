// SPDX-License-Identifier: GPL-3.0
pragma solidity 0.8.0;

import "OpenZeppelin/openzeppelin-contracts@4.5.0/contracts/utils/math/Math.sol";

uint constant PAGE_SIZE = 10;

contract PostModel
{
  struct Post
  {
    uint post_id;
    address username;
    string title;
    string text;
    string link;
    uint date_created;
    uint score;
    //upvotedby: [ { type: mongoose.Schema.ObjectId, ref: 'User' } ],
    //downvotedby: [ { type: mongoose.Schema.ObjectId, ref: 'User' } ]
  }

  //TODO: add mapping that maps original post_id to rotated_id when a post is deleted
  Post[] posts;
  uint public posts_index = 0;

  function addPost(string memory title, string memory text, string memory link) public
  {
    uint score = 0;
    uint date_created = block.timestamp;
    Post memory element = Post(posts_index, msg.sender, title, text, link, date_created, score);

    posts.push(element);
    posts_index++;
  }

  function removePost(uint id) public
  {
    require(id < posts_index, "need valid post id");

    posts[id] = posts[posts_index - 1];
    posts.pop();
    posts_index--;
  }

  function getPost(uint id) public view returns(Post memory)
  {
    require(id < posts_index, "need valid post id");

    return posts[id];
  }

  function getAllPosts(uint page) public view returns(Post[PAGE_SIZE] memory)
  {
    Post[PAGE_SIZE] memory ret_data;
    uint starting_index = page * PAGE_SIZE;
    uint last_index = Math.min(posts_index, starting_index + PAGE_SIZE);
    require(starting_index < posts_index, "need valid page number");

    for(uint i = starting_index; i < last_index; i++)
    {
      ret_data[i - starting_index] = posts[i];
    }

    return ret_data;
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
