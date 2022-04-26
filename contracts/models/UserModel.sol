// SPDX-License-Identifier: GPL-3.0
pragma solidity 0.8.0;

library UserStruct
{
  struct User
  {
    address username;
    string name;
    string email;
    bool banned;
    bool shadowed;
    bool isAdmin;
    uint date_created;
    //upvotes: [ { type: mongoose.Schema.ObjectId, ref: 'Post' } ],
    //downvotes: [ { type: mongoose.Schema.ObjectId, ref: 'Post' } ]
  }
}

contract UserModel
{
  mapping(address => UserStruct.User) users;
  uint public count = 0;

  function addUser(string memory name, string memory email) public
  {
    uint date_created = block.timestamp;

    users[tx.origin] = UserStruct.User(tx.origin, name, email, false, false, false, date_created);
    count++;
  }

  function getUser(address username) public view returns(UserStruct.User memory)
  {
    return users[username];
  }

  //TODO: restrict caller
  function updateUser(UserStruct.User memory updated_user) public
  {
    users[updated_user.username] = updated_user;
  }

  //TODO: restrict caller
  function removeUser(address username) public
  {
    delete users[username];
    count--;
  }

  function doesUserExist(address username) public view returns (bool)
  {
    uint user_date_created = users[username].date_created;
    return user_date_created != 0;
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
