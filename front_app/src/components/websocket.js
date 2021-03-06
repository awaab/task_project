import React, { Component } from 'react'
import { type } from 'jquery';

const socketPath = 'wss://' + window.location.host + "/ws/status/";
//const socketPath = 'ws://echo.websocket.org/';

class WebsocketComponent extends Component {
constructor(props){
   super(props);
}
refreshDisplay = () =>{
    this.props.setStatus("CONNECTED");
}
setupWebSocket = () =>{
    this.ws = new WebSocket(socketPath);
    this.ws.onopen = () => {
        console.log('ws connected');
        this.props.setStatus("CONNECTED");
      }
  
      this.ws.onmessage = (evt) => {
        const data = JSON.parse(evt.data);
        this.props.setStatus(data.message);
        // Remove message and display default
        setTimeout(this.refreshDisplay, 2000);
      }
  
      this.ws.onclose = () => {
        this.props.setStatus("DISCONNECTED");
        if(this.props.loggedIn()){
          console.log("this.props.loggedIn",this.props.loggedIn);
        console.log('Disconnected, trying to reconnect.')
        setTimeout(this.setupWebSocket, 2000);
        }
      }
}
    
  componentDidMount() {
    this.setupWebSocket();    
  }

  render() {
    return (
      <div>
      </div>
    )
  }
}

export default WebsocketComponent;
