import React from 'react'
import PropTypes from 'prop-types'
import SurveyItem from './SurveyItem'
import './SurveyList.css'

class SurveyList extends React.Component {
  render () {
    let surveys = this.props
    console.log(surveys)
    console.log(Object.keys(surveys).length)
    return (
      <div className='SurveyList row'>
        <ul className='list-unstyled'>
            {Object.keys(surveys).map((item, i) =>
                <SurveyItem {...surveys[item]}>
                </SurveyItem>
            )}
        </ul>
      </div>
    )
  }
}

SurveyList.propTypes = {
  surveys: PropTypes.array.isRequired
}

export default SurveyList
