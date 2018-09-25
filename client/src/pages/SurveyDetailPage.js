import React, { Component } from 'react'
import { connect } from 'react-redux'
import SurveyNavBar from './../containers/SurveyNavBar'
import { fetchSurvey } from '../actions/survey'

class SurveyDetailPage extends Component {
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
    console.log(this.props)
    return (
      <div>
        <p>
          {this.props.surveyId}
        </p>
      </div>
    )
  }
}

const mapStateToProps = (state) => {
  console.log(state)
  return {
    Survey: state.fetchSurvey
  }
}

export default connect(mapStateToProps, (state, { params }) => ({
  surveyId: params.surveyId
}), {
  fetchSurvey
})(SurveyDetailPage)
