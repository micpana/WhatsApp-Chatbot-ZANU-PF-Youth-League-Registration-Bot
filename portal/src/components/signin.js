import React, { Component, useReducer } from 'react';
import {Collapse,Navbar,NavbarToggler,NavbarBrand,Nav,NavItem,NavLink,UncontrolledDropdown,
 Button, Input, Row, Col, Dropdown, DropdownToggle, DropdownMenu, DropdownItem, Table, Form, FormGroup, Container, Label, InputGroup} from "reactstrap";
import { withCookies, Cookies } from 'react-cookie';
import { instanceOf } from 'prop-types';
import axios from 'axios';
import {Helmet} from 'react-helmet'
import {Backend_Url} from './backend_url'
import Background_Image from '../images/image_1.jpg'

  class Signin extends Component{
    static propTypes = {
        cookies: instanceOf(Cookies).isRequired
    };
    constructor(props) { 
      super(props);
      this.state = {
        phonenumber: '',
        password: ''
    };


    this.SignIn = (e) => {
        e.preventDefault()
        const { cookies } = this.props
        var phonenumber = this.state.phonenumber
        var password = this.state.password

        var data = new FormData() 
        data.append('phonenumber', phonenumber)
        data.append('password', password)
        
        axios.post(Backend_Url + 'signin', data)
        .then((res) => {
            let result = res.data
            if(result.status == 'Signin failed, incorrect details entered'){
                alert('Incorrent details entered.')
            }else if(result.status == 'Signin successful'){
                cookies.set('token', result.access_token, { path: '/' })
                let port = (window.location.port ? ':' + window.location.port : '')
                window.location.href = '//' + window.location.hostname + port + '/dashboard'
            }else{
                alert('An network error has occured, please try again.')
            }
        }).catch((error) => {
            alert('SignIn failed, please check your details and try again.')
        })
      }

    ///////////handle text fields change
    this.HandleChange = (e) =>{
        this.setState({[e.target.name]: e.target.value});
    };//////handle change ends here
    }

    componentDidMount() {
      const { cookies } = this.props;
      if(cookies.get('token')!=null){
        let port = (window.location.port ? ':' + window.location.port : '');
        window.location.href = '//' + window.location.hostname + port + '/dashboard';
      };
  }

    render() {
      return (
        <div style={{backgroundImage: "url(" + Background_Image + ")"}}>
          <div style={{opacity: '0.9', backgroundColor: '#E0DBDF', minHeight: '630px'}}>
            <Helmet>
              <title>Sign In</title>
              {/* <meta name="description" content="" /> */}
            </Helmet>
            <Row style={{margin: '0px'}}>
              <Col sm='5'>
              <Form onSubmit={this.SignIn} >
                <Container style={{paddingRight: '100px', paddingLeft: '100px'}}>
                <br/><br/><br/><br/><br/>
                <Row>
                  <Col>
                    <h4 style={{color: '#1faced', fontWeight: 'bold'}}>Sign In</h4>
                  </Col>
                </Row>
                <br/><br/>
                <Row>
                  <Col>
                    <InputGroup>
                      <Input  style={{border: 'none', borderBottom: '1px solid #1faced', color: 'inherit', backgroundColor: 'inherit'}} placeholder="Phonenumber e.g +263782345678" type="text" name="phonenumber" id="phonenumber" 
                      value={this.state.phonenumber} onChange={this.HandleChange} />
                    </InputGroup> 
                  </Col>
                </Row>
                <br/><br/>
                <Row>
                  <Col>
                    <InputGroup>
                      <Input  style={{border: 'none', borderBottom: '1px solid #1faced', color: 'inherit', backgroundColor: 'inherit'}} placeholder="Password" type="password" name="password" id="password" 
                      value={this.state.password} onChange={this.HandleChange} />
                    </InputGroup> 
                  </Col>
                </Row>
                <br/><br/><br/>
                <Button type="submit" style={{backgroundColor: '#1faced', color: '#FFFFFF', border: 'none', borderRadius: '20px', fontWeight: 'bold', width: '120px'}}>SignIn</Button>{' '}
                <Button color="secondary" href="/" style={{backgroundColor: '#1faced', color: '#FFFFFF', border: 'none', borderRadius: '20px', fontWeight: 'bold', width: '120px'}}>Cancel</Button>
                </Container>
                </Form>
              </Col>
              <Col style={{backgroundColor: '#1faced', minHeight: '630px', color: '#FFFFFF'}}>
                <h3 style={{marginTop: '170px'}}>
                  ZANUPF YOUTH LEAGUE
                </h3>
              </Col>
            </Row>
          </div>
        </div>
      );
    }

  };
  
  export default withCookies(Signin);