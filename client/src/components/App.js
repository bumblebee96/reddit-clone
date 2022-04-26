import React, { Component } from "react";
import Homepage from "./Homepage";
import Submit from "./Submit";
import Single from "./Single";
import Register from "./Register";
import Admin from "./Admin";
import { BrowserRouter, Route, Link, Redirect } from "react-router-dom";
import UserPage from "./UserPage";
import InnerHTML from "react-dangerous-html";

import {getWeb3} from "../getWeb3"
import map from "../artifacts/deployments/map.json"
import {getEthereum} from "../getEthereum"


function Layout(props) {
  return <div id="layout">{props.children}</div>;
}

export default class App extends Component {

  state = {
    web3: null,
    accounts: null,
    chainid: null,
    commentModel: null,
    postModel: null,
    userModel: null,
    commentController: null,
    postController: null,
    userController: null,

    loading: true,
    posts: [],
    user: {},
    token: "",
    loggedIn: false,
    loginError: false,
    loginMsg: "Something went wrong",
    currentPage: 1,
    loadMore: true,
    codes: null,
  };

  getNextPosts = () => {
    let posts = [...this.state.posts];
    fetch(`/api/posts/50/${this.state.currentPage}`)
      .then((res) => res.json())
      .then((res) => {
        if (res.posts.length) {
          res.posts.forEach((post) => {
            posts.push(post);
          });
          this.setState({ posts, currentPage: this.state.currentPage + 1 });
          console.log(res);
        } else {
          console.log("End of the posts");
          this.setState({ loadMore: false });
        }
      })
      .catch((err) => console.log(err));
  };

  register = (res) => {
    this.setState({
      loggedIn: true,
      user: res.user,
      token: res.token,
    });
    let userInfo = {
      loggedIn: true,
      user: res.user,
      token: res.token,
    };
    localStorage.setItem("userInfo", JSON.stringify(userInfo));
  };

  tokenExpired = () => {
    this.logout();
  };

  login = (event) => {
    event.preventDefault();
    let user = {};
    user.username = event.target.username.value;
    user.password = event.target.password.value;
    if (user.username && user.password) {
      fetch("/api/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(user),
      })
        .then((res) => res.json())
        .then((res) => {
          if (res.success) {
            // login successfully
            this.setState({
              loggedIn: true,
              user: res.user,
              token: res.token,
            });
            let userInfo = {
              loggedIn: true,
              user: res.user,
              token: res.token,
            };
            localStorage.setItem("userInfo", JSON.stringify(userInfo));
          } else {
            this.setState({
              loginError: true,
              loginMsg: res.message,
            });
          }
        })
        .catch((err) => {
          // Catch the error
          console.log(err);
          this.setState({
            loginError: true,
            loginMsg: err,
          });
        });
    } else {
      this.setState({
        loginError: true,
        loginMsg: "Missing credentials",
      });
    }
  };

  logout = () => {
    this.setState({
      loggedIn: false,
      token: undefined,
      user: {},
    });
    localStorage.removeItem("userInfo");
  };

  submitPost = (res) => {
    let posts = [...this.state.posts];
    posts.push(res.post);
    this.setState({ posts, user: res.user });
    localStorage.setItem("posts", JSON.stringify(posts));
  };

  // Update user after up/downvote
  updateUser = (res) => {
    let posts = [...this.state.posts];
    posts.forEach((post, index) => {
      if (post._id === res.post._id) {
        posts[index] = res.post;
      }
    });

    this.setState({ posts });
  };

  deletePost = (res) => {
    let posts = [...this.state.posts];
    posts.forEach((post, index) => {
      if (post._id === res.deletedId) {
        posts.splice(index, 1);
      }
    });
    this.setState({ posts });
  };

  componentDidMount = async () => {
    // Get network provider and web3 instance.
    const web3 = await getWeb3()

    // Try and enable accounts (connect metamask)
    try {
        const ethereum = await getEthereum()
        ethereum.enable()
    } catch (e) {
        console.log(`Could not enable accounts. Interaction with contracts not available.
        Use a modern browser with a Web3 plugin to fix this issue.`)
        console.log(e)
    }

    const accounts = await web3.eth.getAccounts()
    const chainid = parseInt(await web3.eth.getChainId())

    this.setState({
      web3: web3,
      accounts: accounts,
      chainid: chainid
    }, await this.loadInitialContracts)

    let userInfo = JSON.parse(localStorage.getItem("userInfo"));

    if (userInfo) {
      this.setState({
        loggedIn: true,
        token: userInfo.token,
        user: userInfo.user,
      });
    }

    fetch("/api/posts/all")
      .then((res) => res.json())
      .then((res) => {
        if (res.success) {
          this.setState({ posts: res.data, loading: false });
          if (res.data.length < 50) {
            this.setState({ loadMore: false });
          }
        } else {
          console.log("Cannot load the file");
          this.setState({ loading: false });
        }
      })
      .catch((err) => {
        console.log(err);
        this.setState({ loading: false });
      });

    fetch("/api/app/content")
      .then((res) => res.json())
      .then((json) => {
        if (json.success) {
          this.setState({ codes: json.codes });
        }
        // See if you can do anything with errors
      })
      .catch((err) => console.log(err));
  }

  loadInitialContracts = async () => {
        // <=42 to exclude Kovan, <42 to include kovan
        if (this.state.chainid < 42) {
            // Wrong Network!
            return
        }
        console.log(this.state.chainid)

        var _chainID = 0;
        if (this.state.chainid === 42){
            _chainID = 42;
        }
        if (this.state.chainid === 1337){
            _chainID = "dev"
        }
        console.log(_chainID)

        const commentModel = await this.loadContract(_chainID,"CommentModel")
        const postModel = await this.loadContract(_chainID,"PostModel")
        const userModel = await this.loadContract(_chainID,"UserModel")
        const commentController = await this.loadContract(_chainID,"CommentController")
        const postController = await this.loadContract(_chainID,"PostController")
        const userController = await this.loadContract(_chainID,"UserController")

        if (!commentModel ||
            !postModel ||
            !userModel ||
            !commentController ||
            !postController ||
            !userController) {
            return
        }

        this.setState({
            commentModel: commentModel,
            postModel: postModel,
            userModel: userModel,
            commentController: commentController,
            postController: postController,
            userController: userController,
        })
    }

    loadContract = async (chain, contractName) => {
        // Load a deployed contract instance into a web3 contract object
        const {web3} = this.state

        // Get the address of the most recent deployment from the deployment map
        let address
        try {
            address = map[chain][contractName][0]
        } catch (e) {
            console.log(`Couldn't find any deployed contract "${contractName}" on the chain "${chain}".`)
            return undefined
        }

        // Load the artifact with the specified address
        let contractArtifact
        try {
            contractArtifact = await import(`../artifacts/deployments/${chain}/${address}.json`)
        } catch (e) {
            console.log(`Failed to load contract artifact "../artifacts/deployments/${chain}/${address}.json"`)
            return undefined
        }

        return new web3.eth.Contract(contractArtifact.abi, address)
    }

  render() {

    if (!this.state.web3) {
        return <div>Loading Web3, accounts, and contracts...</div>
    }

    // <=42 to exclude Kovan, <42 to include Kovan
    if (isNaN(this.state.chainid) || this.state.chainid < 42) {
        return <div>Wrong Network! Switch to your local RPC "Localhost: 8545" in your Web3 provider (e.g. Metamask)</div>
    }

    if (!this.state.commentModel ||
        !this.state.postModel ||
        !this.state.userModel ||
        !this.state.commentController ||
        !this.state.postController ||
        !this.state.userController) {
        return <div>Could not find a deployed contract. Check console for details.</div>
    }

    return (
      <BrowserRouter>
        <Layout>
          <header id="header">
            <nav className="top-menu" />
            <div className="main-header">
              <Link to="/" id="header-img" className="default-header">
                reddit clone
              </Link>
              <div className="tab-menu" />

              <div className="user-header">
                {this.state.loggedIn && this.state.user.isAdmin ? (
                  <span>
                    {" "}
                    <Link to="/admin">Admin Settings</Link> |{" "}
                  </span>
                ) : (
                  ""
                )}
                {this.state.loggedIn ? (
                  <span>
                    Hello{" "}
                    <Link
                      className="fake-link"
                      to={`/user/${this.state.user.username}`}
                    >
                      {this.state.user.username}
                    </Link>{" "}
                    |{" "}
                    <a className="fake-link" onClick={this.logout}>
                      logout
                    </a>{" "}
                  </span>
                ) : (
                  <span>
                    Want to join? <Link to="/register">sign up</Link> in
                    seconds.
                  </span>
                )}
              </div>
            </div>
          </header>
          <div id="container">
            <main id="body-submissions">
              {this.state.codes ? (
                <div className="banner top-banner padding">
                  <InnerHTML html={this.state.codes.topBanner} />
                </div>
              ) : (
                ""
              )}
              <Route
                exact
                path="/"
                render={(props) => (
                  <Homepage
                    loading={this.state.loading}
                    user={this.state.user}
                    posts={this.state.posts}
                    token={this.state.token}
                    updateUser={this.updateUser}
                    deletePost={this.deletePost}
                    getNextPosts={this.getNextPosts}
                    currentPage={this.state.currentPage}
                    loadMore={this.state.loadMore}
                    {...props}
                  />
                )}
              />
              <Route
                path="/submit"
                render={(props) =>
                  this.state.loggedIn ? (
                    <Submit
                      user={this.state.user}
                      token={this.state.token}
                      tokenExpired={this.tokenExpired}
                      submitPost={this.submitPost}
                      {...props}
                    />
                  ) : (
                    <Redirect to="/" />
                  )
                }
              />
              <Route
                path="/admin"
                render={(props) =>
                  this.state.loggedIn && this.state.user.isAdmin ? (
                    <Admin
                      {...props}
                      token={this.state.token}
                      codes={this.state.codes}
                    />
                  ) : (
                    <Redirect to="/" />
                  )
                }
              />
              <Route
                exact
                path="/user/:username"
                render={(props) => (
                  <UserPage
                    user={this.state.user}
                    posts={this.state.posts}
                    token={this.state.token}
                    updateUser={this.updateUser}
                    deletePost={this.deletePost}
                    {...props}
                  />
                )}
              />
              <Route
                exact
                path="/post/:id"
                render={(props) => (
                  <Single
                    user={this.state.user}
                    token={this.state.token}
                    banner={
                      this.state.codes ? this.state.codes.commentBanner : null
                    }
                    updateUser={this.updateUser}
                    deletePost={this.deletePost}
                    posts={this.state.posts}
                    {...props}
                  />
                )}
              />
              <Route
                path="/register"
                render={(props) =>
                  this.state.loggedIn ? (
                    <Redirect to="/" />
                  ) : (
                    <Register register={this.register} {...props} />
                  )
                }
              />
            </main>
            <aside id="sidebar">
              {/*
              <form action="">
                <input className="search" type="text" placeholder="Search" />
              </form>

              */}

              {this.state.loggedIn ? (
                ""
              ) : (
                <div className="login-box" id="login">
                  {this.state.loginError ? (
                    <div className="login-error">
                      {this.state.loginMsg}
                      <div
                        className="close-button"
                        onClick={() => {
                          this.setState({ loginError: false });
                        }}
                      >
                        &times;
                      </div>
                    </div>
                  ) : (
                    ""
                  )}
                  <form onSubmit={this.login}>
                    <input
                      className="login-username"
                      type="text"
                      name="username"
                      placeholder="username"
                      required
                    />
                    <input
                      className="login-password"
                      type="password"
                      name="password"
                      placeholder="password"
                      required
                    />
                    <div className="login-button-area">
                      <a className="login-reset-link" href="/reset">
                        reset password
                      </a>
                      <button>login</button>
                    </div>
                  </form>
                </div>
              )}
              {this.state.loggedIn ? (
                <div className="submit-button">
                  <Link to="/submit">Submit</Link>
                </div>
              ) : (
                ""
              )}
              {this.state.codes ? (
                <div className="sidebar-ad">
                  <div className="banner sidebar-banner">
                    <InnerHTML html={this.state.codes.sidebarBanner} />
                  </div>
                </div>
              ) : (
                ""
              )}
              {this.state.codes ? (
                <div className="rules-section">
                  <InnerHTML html={this.state.codes.rulesCode} />
                </div>
              ) : (
                ""
              )}
              {this.state.codes ? (
                <div className="html-section">
                  <InnerHTML html={this.state.codes.extraCode} />
                </div>
              ) : (
                ""
              )}
              <p>
                User: demo
                <br />
                Pass: 1234
              </p>
            </aside>
          </div>
          <footer className="center" id="footer">
            {this.state.codes ? (
              <div className="banner footer-banner padding">
                <InnerHTML html={this.state.codes.footerBanner} />
              </div>
            ) : (
              ""
            )}
            <div className="copyright" />
          </footer>
        </Layout>
      </BrowserRouter>
    );
  }
}
