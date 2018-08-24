import React, { Component } from 'react'
import '../css/style.css'

class Surveys extends Component {
  render () {
    return (
      <div className='Surveys'>
        <p> Surveys Test</p>
        {this.props.children}
      </div>
    )
  }
}

export default Surveys
