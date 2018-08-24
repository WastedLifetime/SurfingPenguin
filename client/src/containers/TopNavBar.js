/* global location */
/* eslint no-restricted-globals: ["off", "location"] */

import React, { Component } from 'react'
import { connect } from 'react-redux'
import { withRouter } from 'react-router'
import {Navbar, Nav, NavItem, NavDropdown, MenuItem} from 'react-bootstrap'
import './TopNavBar.css'

class TopNavBar extends Component {
  loginView () {
    let { currentUser } = this.props
    return (
      <Nav pullRight>
        <NavDropdown eventKey={3} title={currentUser.substring(7)} id='basic-nav-dropdown'>
          <MenuItem divider />
          <MenuItem href='#/logout'>Logout</MenuItem>
        </NavDropdown>
      </Nav>
    )
  }

  unLoginView () {
    return (
      <Nav pullRight>
        <NavItem eventKey={1} href='#/login'>Login</NavItem>
        <NavItem eventKey={1} href='#/register'>Register</NavItem>
      </Nav>

    )
  }

  render () {
    // eslint-disable-next-line
    let indexPathname = '#/'
    let surveyPathname = '#/surveys'
    let { currentUser } = this.props
    // if (currentUser) { indexPathname = '#/surveys' }
    return (
      <Navbar className='TopNavBar'>
        <Navbar.Header>
          <Navbar.Brand>
            <a href={indexPathname}>
                Surfing Penguin
            </a>
          </Navbar.Brand>
          <Navbar.Toggle />
        </Navbar.Header>
        <Nav>
          <NavItem href={surveyPathname}>Surveys</NavItem>
        </Nav>
        <Navbar.Collapse>
          {currentUser ? this.loginView() : this.unLoginView()}
        </Navbar.Collapse>
      </Navbar>
    )
  }
}

var mapStateToProps = (state) => {
  return {
    currentUser: state.session.user
  }
}

let topNavBar = withRouter(connect(mapStateToProps)(TopNavBar))

export default topNavBar
