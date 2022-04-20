// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.4.16 <0.7.0;

contract PostController
{
  //postController.verifyToken = async (req, res, next) => {
  //postController.checkIfUserExistsAndIsNotBanned = async (req, res, next) => {
  //postController.getAllPosts = async (req, res) => {
  //postController.getNextPosts = async (req, res) => {
  //postController.submitNewPost = async (req, res) => {
  //postController.getSinglePostAndComments = async (req, res) => {
  //postController.upvote = async (req, res) => {
  //postController.downvote = async (req, res) => {
  //postController.deletePost = async (req, res) => {
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
