// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.4.16 <0.7.0;

contract CommentController
{
  //commentController.allComments = async (req, res) => {
  //commentController.submitComment = async (req, res) => {
  //commentController.deleteComment = async (req, res) => {
  //commentController.upvote = async (req, res) => {
  //commentController.downvote = async (req, res) => {
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
