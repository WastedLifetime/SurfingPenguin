import React, { Component } from 'react'
import './css/style.css'

import TopNavBar from './containers/TopNavBar'

class App extends Component {
  render () {
    return (
      <div className='App'>
        <TopNavBar />
        { this.props.children }
      </div>
    )
  }
}

export default App
