import React from 'react';
import axios from 'axios';
import { Button,Form,Row, Col, Container } from 'react-bootstrap';

const csrf_url = "csrf/";
const base_url = "http://127.0.0.1:8000/";
const login_url = "login/";
const signup_url = "signup/";
const logged_in_check_url = "logged_in/";

class LoginForm extends React.Component {
  constructor(props){
    super(props);
 }
    handleLogin = (event) =>{
      event.preventDefault();
      console.log(event.target.name.value)
      const data = {
            password: event.target.password.value,
            username: event.target.username.value,
        }
      axios.post(login_url, data, )
      .then(res => {
        const resp_data = res.data;
        console.log(resp_data);
        this.props.setLoggedIn(true);
        this.props.setStatus("logged_in");
      })
      
    }

    handleRegister = (event) =>{
      event.preventDefault();
        console.log(event.target.name.value);
        const data = {
            username: event.target.username.value,
              password1: event.target.password.value,
              password2: event.target.password.value,
              email: event.target.email.value,
          }
          axios.post(signup_url, data)
          .then(res => {
            const resp_data = res.data;
            this.props.setLoggedIn(true);
          })
    }
  
    render() {
      return (
          <div>
        <Container className="text-center" style={{width: "75%", marginTop: "3%"}}>
			  <h4 as={Row}>Login</h4>
				<Form onSubmit={this.handleLogin}>
				<Form.Group as={Row} controlId="username">
				    <Form.Control type="text" placeholder="User Name"/>
				  </Form.Group>
				  <Form.Group as={Row} controlId="password">
				   <Form.Control type="password" placeholder="Password"/>
				  	</Form.Group>
					  

				  <Container>
				  <Button variant="primary" type="submit" className="login-button">Login</Button>
				  </Container>
				</Form>
				</Container>

        <Container className="text-center" style={{width: "75%", marginTop: "3%"}}>
			  <h4 as={Row}>New account</h4>
				<Form onSubmit={this.handleRegister}>
				<Form.Group as={Row} controlId="username">
				    <Form.Control type="text" placeholder="User Name"/>
				  </Form.Group>
          <Form.Group as={Row} controlId="email">
				   <Form.Control type="email" placeholder="Email"/>
				  	</Form.Group>
				  <Form.Group as={Row} controlId="password">
				   <Form.Control type="password" placeholder="Password"/>
				  	</Form.Group>
					  <Container>
				  <Button variant="primary" type="submit" className="login-button">Register</Button>
				  </Container>
				</Form>
				</Container>
    </div>
      );
    }
  }
  export default LoginForm;