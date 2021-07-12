import React, { Component, useReducer } from 'react';
import {Collapse, DashboardToggler,DashboardBrand,Nav,NavItem,NavLink,UncontrolledDropdown,
 Button, Input, Row, Col, Dropdown, DropdownToggle, DropdownMenu, DropdownItem, Form, Container, Label, InputGroup} from "reactstrap";
import axios from 'axios';
import { withCookies, Cookies } from 'react-cookie';
import { instanceOf } from 'prop-types';
import {Helmet} from 'react-helmet'
import {Backend_Url} from './backend_url'
import Background_Image from '../images/image_1.jpg'
import Logo from '../images/logos/logo.jpg'
import {CgImport} from 'react-icons/cg'
import {AiOutlineLineChart} from 'react-icons/ai'
import {CgNotes} from 'react-icons/cg'
import {BiUserCircle} from 'react-icons/bi'

  class Dashboard extends Component{
    static propTypes = {
      cookies: instanceOf(Cookies).isRequired
    };
    constructor(props) { 
      super(props);
      this.state = {
        user_details: {}
      };

      this.Signout = () =>{
        const { cookies } = this.props;

        axios.get(Backend_Url + 'deactivateAccessToken/' + cookies.get('token'))
        .then(res => {
          cookies.remove('token', { path: '/' });
          let port = (window.location.port ? ':' + window.location.port : '');
          window.location.href = '//' + window.location.hostname + port + '/';
        })
        .catch((error) => {
          alert('A network error occured while trying to sign you out, please try again.')
        });
      };

      this.dtoggle = () => {
        this.setState(prevState => ({
          dropdownOpen2: !prevState.dropdownOpen
        }));
      }

      this.onMouseEnter = () => {
        this.setState({dropdownOpen: true});
      };
    
      this.onMouseLeave = () => {
        this.setState({dropdownOpen: false});
      };
    }

    componentDidMount() {
      const { cookies } = this.props;
      if(cookies.get('token')==null){
        let port = (window.location.port ? ':' + window.location.port : '');
        window.location.href = '//' + window.location.hostname + port + '/';
      }else{

        axios.get(Backend_Url + 'getUserDetailsByAccessToken/' + cookies.get('token'))
        .then(res => {
          this.setState({
            user_details: res.data
          });
        })
        .catch((error) => {
          console.log(error);
        });
      }
    }




    render() {
      return (
        <div style={{backgroundImage: "url(" + Background_Image + ")"}}>
            <Helmet>
              <title>Dashboard</title>
              {/* <meta name="description" content="" /> */}
            </Helmet>
            <div style={{backgroundColor: '#E0DBDF', opacity: 0.9}}>
                <Row style={{marginRight: '0px'}}>
                    <Col sm='2' style={{minHeight: '630px', backgroundColor: '#1faced', color: '#ffffff', textAlign: 'left'}}>
                        <Container style={{textAlign: 'left'}}>
                            <br/>
                            <img src={Logo} style={{width: '20%'}}/> Youth League
                            <div style={{border: '1px solid #F2B027', marginTop: '5px'}}></div>
                            <br/>
                        </Container>
                        <br/>
                    </Col>
                    <Col>
                        <Row style={{textAlign: 'right', marginRight: '0px', backgroundColor: '#278eba', height: '60px'}}>
                            <Container style={{textAlign: 'right'}}>
                                <Dropdown className="d-inline-block" onMouseOver={this.onMouseEnter} onMouseLeave={this.onMouseLeave} isOpen={this.state.dropdownOpen} toggle={this.dtoggle}>
                                    <DropdownToggle  style={{marginTop: '', backgroundColor:  'inherit', border: 'none', fontSize: '10px', color: '#ffffff'}}>
                                        <BiUserCircle size='25px'/>
                                        <br/>
                                        <span style={{fontWeight: 'bold'}}>
                                          {this.state.user_details.firstname} {this.state.user_details.lastname}
                                        </span>
                                    </DropdownToggle>
                                    <DropdownMenu>
                                        <DropdownItem  onClick={this.Signout}>
                                            <NavLink style={{color: '#1faced', backgoundColor: 'inherit'}} >
                                                Signout
                                            </NavLink>
                                        </DropdownItem>
                                    </DropdownMenu>
                                </Dropdown>
                            </Container>
                        </Row>
                        <Row style={{marginRight: '0px'}}>
                            <Container>
                              <br/>
                              <h6></h6>
                              <br/><br/>
                              <a href={Backend_Url + 'downloadDatabase'} style={{marginTop: '60px'}}>
                                Click here to download the membership database as an excel file.
                              </a>
                            </Container>
                        </Row>
                    </Col>
                </Row>
            </div>
        </div>
      );
    }

  };
  
  export default withCookies(Dashboard);