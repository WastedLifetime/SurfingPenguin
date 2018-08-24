import React from 'react'

class HomePage extends React.Component {
  render () {
    return (
      <div>
        <p> HomePage Test </p>
        {this.props.children}
      </div>
    )
  }
}

export default HomePage
