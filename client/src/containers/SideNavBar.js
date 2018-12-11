/* eslint no-restricted-globals: ['off', 'location'] */

import React, { Component } from 'react'
import { connect } from 'react-redux'
import { withRouter } from 'react-router'
import {Nav, NavDropdown, MenuItem} from 'react-bootstrap'
import '../css/style.css'
import './SideNavBar.css'

class SideNavBar extends Component {
  render () {
    let { currentUser } = this.props
    // if (currentUser) { indexPathname = '#/surveys' }
    return (
      <Nav pullRight bsStyle='SideNavBar'>

        <NavDropdown title={<span class='glyphicon glyphicon-user' aria-hidden='true'> {currentUser} </span>}>
          <MenuItem href='#/logout'>Logout </MenuItem>
          <MenuItem href='#/' active>Donate</MenuItem>
          <MenuItem divider />
          <MenuItem href='#/logout'>登出 </MenuItem>
          <MenuItem href='#/' active>Donate</MenuItem>
        </NavDropdown>
      </Nav>
    )
  }
}

var mapStateToProps = (state) => {
  return {
    currentUser: state.session.user
  }
}

let sideNavBar = withRouter(connect(mapStateToProps)(SideNavBar))

export default sideNavBar
