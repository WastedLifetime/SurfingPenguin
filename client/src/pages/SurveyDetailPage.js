import React, { Component } from 'react'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import { getSurvey, getFetchError, getFetchStatus, getSubmitStatus } from '../reducers/survey'
import Survey from '../components/Survey/Survey'
import SurveyNavBar from './../containers/SurveyNavBar'
import { fetchSurvey } from '../actions/survey'

class SurveyDetailPage extends Component {
  loaddata () {
    this.props.fetchsurvey(this.props.surveyid)
  }

  componentdidmount () {
    this.loaddata()
  }

  componentdidupdate (prevprops) {
    if (this.props.surveyid !== prevprops.surveyid) {
      this.loaddata()
    }
  }
  render () {
    let {id, questoin_num, surveyname, survey_description, prize_description} = this.props.survey
    console.log(this.props.survey.questions)
    return (
      <div>
        <h1>Survey {id} {surveyname}</h1>
        <table>
          <p>survey description: {survey_description}</p>
          <p>prize description: {prize_description}</p>
          <p>questions: {this.props.survey.questions}</p>
        </table>
      </div>
    )
  }
}

const mapStateToProps = (state, { params }) => {
  return {
    survey: getSurvey(state.survey),
    isLoading: getFetchStatus(state.survey),
    surveyId: params.surveyId,
    isSuccess: getSubmitStatus(state.survey)
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
    fetchSurvey: bindActionCreators(fetchSurvey, dispatch)
  }
}
export default connect(mapStateToProps, mapDispatchToProps)(SurveyDetailPage)
