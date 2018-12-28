import React from 'react'
import NewSurvey from '../containers/NewSurvey'
import SurveyList from '../containers/SurveyList'
import './NewSurveyPage.css'

class NewSurveysPage extends React.Component {
  render () {
    return (
      <div className='container NewSurveysPage'>
        <NewSurvey />
        <SurveyList />

      </div>
    )
  }
}

export default NewSurveysPage
