// SPDX-License-Identifier: GPL-3.0
pragma solidity 0.8.0;

import "../models/PostModel.sol";
import "../models/UserModel.sol";

contract UserController
{
  enum AdminAction
  {
    ban,
    unban,
    makeadmin,
    removeadmin
  }

  UserModel um;

  constructor()
  {
    //TODO: set address of user model contract in config
    um = UserModel(msg.sender);
  }

  function register(string memory name, string memory email) public
  {
    bool user_already_exists = um.doesUserExist(msg.sender);
    require(!user_already_exists, "The username is already taken");

    um.addUser(name, email);
  }

  function login() public view returns(UserStruct.User memory)
  {
    bool user_already_exists = um.doesUserExist(msg.sender);
    require(user_already_exists, "There is no user with that username");

    return um.getUser(msg.sender);
  }

  function remove() public
  {
    um.removeUser(msg.sender);
    //TODO: remove posts
  }

  function action(address moduser, AdminAction act) public
  {
    bool user_already_exists = um.doesUserExist(msg.sender);
    require(user_already_exists, "There is no user with that username");
    UserStruct.User memory admin_user = um.getUser(msg.sender);
    require(admin_user.isAdmin, "user is not an admin");

    user_already_exists = um.doesUserExist(moduser);
    require(user_already_exists, "There is no user with that username");
    UserStruct.User memory modified_user = um.getUser(moduser);

    if(act == AdminAction.ban)
    {
      modified_user.banned = true;
      modified_user.isAdmin = false;
    }
    else if(act == AdminAction.unban)
    {
      modified_user.banned = false;
    }
    else if(act == AdminAction.makeadmin)
    {
      modified_user.banned = false;
      modified_user.isAdmin = true;
    }
    else if(act == AdminAction.removeadmin)
    {
      modified_user.isAdmin = false;
    }

    um.updateUser(modified_user);
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
