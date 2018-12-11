/* global location */
/* eslint no-restricted-globals: ["off", "location"] */

import React, { Component } from 'react'
import { connect } from 'react-redux'
import { withRouter } from 'react-router'
import {Col, Navbar, Nav, NavItem, NavDropdown, MenuItem} from 'react-bootstrap'
import SideNavBar from './SideNavBar'
import '../css/style.css'
import './TopNavBar.css'

class TopNavBar extends Component {
  loginView () {
    let { currentUser } = this.props
    return (
      <SideNavBar />
    )
  }

  unLoginView () {
    return (
      <Nav pullRight>
        <NavItem eventKey={1} href='#/login'>登入</NavItem>
        <NavItem eventKey={1} href='#/register'>註冊</NavItem>
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
      <Navbar bsStyle='TopNavBar'>
        <Navbar.Header>
          <Navbar.Brand>
            <a href={currentUser ? surveyPathname : indexPathname}>
                Survey Penguin
            </a>
          </Navbar.Brand>
          <Navbar.Toggle />
        </Navbar.Header>
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
