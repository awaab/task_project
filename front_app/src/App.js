import React from 'react';
import logo from './logo.svg';
import './App.css';
import LoginForm from './components/login.js';
import Profile from './components/profile.js';
import WebsocketComponent from './components/websocket.js';
import axios from 'axios';
import getCookie from './cookie';
import 'bootstrap/dist/css/bootstrap.min.css';

const base_url = "http://127.0.0.1:8000/";
const csrf_url = "csrf/";
const logged_in_check_url = "logged_in/";
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.headers.common['Content-Type'] = 'application/json';
axios.defaults.withCredentials = true;

function setCsrfToken() {
  let _csrfToken=getCookie("csrftoken");
  axios.defaults.headers.common['X-CSRFTOKEN'] = _csrfToken;
  console.log(_csrfToken,"_csrfToken")
  }

class App extends React.Component{

setLoggedIn = (logged_in) =>{
  this.setState({logged_in: logged_in});
}
  constructor(props) {
    super(props);
    this.state = {
    logged_in: false,
    status: 'DISCONNECTED',
  };
  
    axios.post(logged_in_check_url)
      .then(response => {
      console.log(response);
      this.setLoggedIn(true);
      this.setStatus("logged_in");
      setCsrfToken();
  }).catch(err => {
    // what now?
    console.log(err);
    setCsrfToken();
});

}
setStatus = (status)=>{
  console.log("************ changng to:",status);
  this.setState({status: status});
}
  render() {
    return (
      <div className="App">
        <h3 style={{marginTop: "1%"}}><span class={dot_class[this.state.status]}></span>
            {this.state.status == "DISCONNECTED" && "Login or register"}
            {this.state.status == "CONNECTED" && "Edit user details"}
            {this.state.status == "CHANGED_DETAILS" && "User details have been set"}
            </h3>
       {!this.state.logged_in && <LoginForm setLoggedIn={this.setLoggedIn} />}
       {this.state.logged_in && <div><WebsocketComponent setStatus={this.setStatus}/><Profile setLoggedIn={this.setLoggedIn}/></div>}
      </div>
    );
  }
}

const dot_class = {
  "DISCONNECTED": "greyDot",
  "CONNECTED": "greenDot",
  "CHANGED_DETAILS": "blueDot",
}
export default App;
