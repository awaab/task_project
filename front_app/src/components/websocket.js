import React, { Component } from 'react'
import { type } from 'jquery';

const socketPath = 'ws://' + window.location.host + "/ws/status/";
//const socketPath = 'ws://echo.websocket.org/';

class WebsocketComponent extends Component {
constructor(props){
   super(props);
}
setupWebSocket = () =>{
    this.ws = new WebSocket(socketPath);
    this.ws.onopen = () => {
        console.log('ws connected');
        this.props.setStatus("CONNECTED");
        this.ws.send(JSON.stringify({abcd:"abcd"}));
      }
  
      this.ws.onmessage = (evt) => {
        const data = JSON.parse(evt.data);
        this.props.setStatus(data.message);
        console.log(typeof(data));
      }
  
      this.ws.onclose = () => {
        this.props.setStatus("DISCONNECTED");
        console.log('Disconnected, trying to reconnect.')
        setTimeout(this.setupWebSocket, 2000);
      }
}
    
  componentDidMount() {
    //this.ws = new WebSocket(socketPath);
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
