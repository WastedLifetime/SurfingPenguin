import React from 'react'
import { connect } from 'react-redux'
import SurveyNavBar from './../containers/SurveyNavBar'
import { fetchSurvey } from '../actions/editSurvey'
import './EditSurveyPage.css'
// TODO: this page is directly from the EditSurvey page and need to be updated

class SharedSurveyPage extends React.Component {
  loadData () {
    this.props.fetchSurvey(this.props.surveyId)
  }

  componentDidMount () {
    this.loadData()
  }

  componentDidUpdate (prevProps) {
    if (this.props.surveyId !== prevProps.surveyId) {
      this.loadData()
    }
  }

  render () {
    return (
      <div>
        <div>
          <SurveyNavBar />
        </div>
        TODO: this page is directly from the EditSurvey page and need to be updated
        {this.props.children}
      </div>
    )
  }
}

export default connect((state, { params }) => ({
  surveyId: params.surveyId
}), {
  fetchSurvey
})(SharedSurveyPage)
