import React from 'react';
import axios from 'axios';
import { Button,Form,Row, Col,Container } from 'react-bootstrap';
import Table from 'react-bootstrap/Table';
const logged_out_url = "logout/";
const userdata_url = "user/";
const logged_in_check_url = "logged_in/";
const submit_data_url = "user/edit/";
class Profile extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      username: "username",
      email: "email",
      phone: 0,
      age: 0,
    };
  }
    componentDidMount(){
        axios.get(userdata_url)
          .then(response => {
          console.log(response);
          this.setUserdata(response.data);
          console.log(this.state);
      });
    }

 setUserdata = (data) =>{
   this.setState({
     username: data.username,
     phone: data.phone_number,
     age: data.age,
     email: data.email,
  });
 }
 submitData = (event) =>{
  event.preventDefault();
  let data = {
    phone_number: event.target.phone.value,
    age: event.target.age.value,
    email: event.target.email.value,
  }
  event.target.phone.value="";
  event.target.age.value="";
  event.target.email.value="";
  axios.post(submit_data_url, data)
  .then(response => {
  console.log(response);
  this.setUserdata(response.data);
});
 }
  handleLogout = (event) =>{
      event.preventDefault();
      axios.post(logged_out_url)
      .then(response => {
      console.log(response);
      this.props.setLoggedIn(false);
  });
    }
    checkLoggedin = (event) =>{
      axios.post(logged_in_check_url)
      .then(response => {
      console.log(response);
      this.setLoggedIn(true);
  });
    }

  
    render() {
      return (
        <div>
  <Container className="text-center" style={{width: "75%", marginTop: "2%"}}>
  <h3>User Info</h3>
  <Table striped bordered hover>
  <tbody>
  <tr>
    <td>Username</td>
    <td>{this.state.username}</td>
  </tr>
  <tr>
    <td>Email</td>
    <td>{this.state.email}</td>
  </tr>
  <tr>
    <td>Phone no.</td>
    <td>{this.state.phone}</td>
  </tr>
  <tr>
    <td>Age</td>
    <td>{this.state.age}</td>
  </tr>
  </tbody>
</Table>
</Container>
<Container className="text-center" style={{width: "75%", marginTop: "2%"}}>
			  <h3 as={Row}>Edit user info</h3>
				<Form onSubmit={this.submitData}>
				<Form.Group as={Row} controlId="email">
				    <Form.Control type="email" placeholder="Email"/>
				  </Form.Group>
          <Form.Group as={Row} controlId="age">
				   <Form.Control type="number" placeholder="Age"/>
				  	</Form.Group>
				  <Form.Group as={Row} controlId="phone">
				   <Form.Control type="number" placeholder="Phone no."/>
				  	</Form.Group>
					  
				  	<Container>
				  <Button variant="primary" type="submit" className="login-button">Submit new user info</Button>
				  </Container>
				  
				</Form>
				</Container>

        <Container style={{marginTop: "2%"}}>
        <Button onClick={this.handleLogout} style={{width: "40%"}}>Logout</Button>
        </Container>

          {/* <button onClick={this.checkLoggedin}>
          Logged in?
          </button> */}
      </div>
      );
    }
  }
  export default Profile;