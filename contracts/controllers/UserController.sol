// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.4.16 <0.7.0;

contract UserController
{
  //userController.validateRegInfo = (req, res, next) => {
  //userController.validateLoginInfo = (req, res, next) => {
  //userController.checkIfUserExists = (req, res, next) => {};
  //userController.register = async (req, res) => {
  //userController.login = async (req, res) => {
  //userController.adminAction = async (req, res) => {
  //userController.deleteUser = async (req, res) => {
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
