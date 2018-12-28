import React from 'react'
import '../css/style.css'

class SupportPage extends React.Component {
  render () {
    return (
      <div>
        <section id='banner'>
          <h2>Support Page</h2>
        </section>
        <section id='one' className='wrapper style1 special'>
          <div className='container'>
            <header className='major'>
              <h2>Consectetur adipisicing elit</h2>
              <p>Lorem ipsum dolor sit amet, delectus consequatur, similique quia!</p>
            </header>
            <div className='row 150%'>
              <div className='4u 12u$(medium)'>
                <section className='box'>
                  <i className='icon big rounded color1 fa-cloud' />
                  <h3>Lorem ipsum dolor</h3>
                  <p>Fix CSS</p>
                </section>
              </div>
              <div className='4u 12u$(medium)'>
                <section className='box'>
                  <i className='icon big rounded color9 fa-desktop' />
                  <h3>Consectetur adipisicing</h3>
                  <p>Fix CSS</p>
                </section>
              </div>
              <div className='4u$ 12u$(medium)'>
                <section className='box'>
                  <i className='icon big rounded color6 fa-rocket' />
                  <h3>Adipisicing elit totam</h3>
                  <p>Fix CSS</p>
                </section>
              </div>
            </div>
          </div>
        </section>
        {this.props.children}
      </div>
    )
  }
}

export default SupportPage
