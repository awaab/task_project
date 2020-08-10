import React, { Component } from 'react'

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
        this.ws.send(JSON.stringify({abcd:"abcd"}));
      }
  
      this.ws.onmessage = (evt) => {
        const message = evt.data;
        console.log(message);
      }
  
      this.ws.onclose = () => {
        console.log('Disconnected, trying to reconnect.')
        setTimeout(this.setupWebSocket, 1000);
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
