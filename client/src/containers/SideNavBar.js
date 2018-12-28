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
          <MenuItem className='dropdown-link' href='#/user/profile'>{currentUser}</MenuItem>
          <MenuItem className='dropdown-link' divider />
          <MenuItem className='dropdown-link' href='#/create_survey'>建立問卷</MenuItem>
          <MenuItem divider />
          <MenuItem className='dropdown-link' href='#/user/my_surveys'>我的問卷</MenuItem>
          <MenuItem className='dropdown-link' href='#/user/shared_surveys'>共用問卷</MenuItem>
          <MenuItem className='dropdown-link' href='#/user/collected_surveys'>收藏問卷</MenuItem>
          <MenuItem divider />
          <MenuItem className='dropdown-link' href='#/user/settings'>設定</MenuItem>
          <MenuItem className='dropdown-link' href='#/support'>支援</MenuItem>
          <MenuItem className='dropdown-link' href='#/contact_us'>聯絡我們</MenuItem>
          <MenuItem className='dropdown-link' href='#/privacy'>隱私權政策</MenuItem>
          <MenuItem divider />
          <MenuItem className='dropdown-link' href='#/logout'>登出 </MenuItem>
          <MenuItem className='dropdown-link' href='#/' active>Donate</MenuItem>
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
