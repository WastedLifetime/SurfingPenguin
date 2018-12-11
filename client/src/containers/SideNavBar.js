/* eslint no-restricted-globals: ['off', 'location'] */

import React, { Component } from 'react'
import { connect } from 'react-redux'
import { withRouter } from 'react-router'
import {Nav, NavDropdown, MenuItem} from 'react-bootstrap'
// import '../css/style.css'
import './SideNavBar.css'

class SideNavBar extends Component {
  render () {
    let { currentUser } = this.props
    currentUser = currentUser.slice(7)
    // if (currentUser) { indexPathname = '#/surveys' }
    return (
      <Nav pullRight bsStyle='SideNavBar'>

        <NavDropdown title={<span class='glyphicon glyphicon-user' aria-hidden='true'> {currentUser} </span>}>
          <MenuItem href='#/user_profile'>{currentUser}</MenuItem>
          <MenuItem divider />
          <MenuItem href='#/create_survey'>建立問卷</MenuItem>
          <MenuItem divider />
          <MenuItem href='#/my_survey'>我的問卷</MenuItem>
          <MenuItem href='#/shared_survey'>共用問卷</MenuItem>
          <MenuItem href='#/collected_survey'>收藏問卷</MenuItem>
          <MenuItem divider />
          <MenuItem href='#/setting'>設定</MenuItem>
          <MenuItem href='#/support'>支援</MenuItem>
          <MenuItem href='#/contact_us'>聯絡我們</MenuItem>
          <MenuItem href='#/privacy'>隱私權政策</MenuItem>
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
