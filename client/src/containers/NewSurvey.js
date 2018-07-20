import React from 'react'
import { connect } from 'react-redux'
import { withRouter } from 'react-router'
import { bindActionCreators } from 'redux'
import NewSurveyView from '../components/NewSurvey'
import { createSurveyRequest, resetCreateSurvey } from '../actions/surveys'
import { Path } from '../routes'

class NewSurvey extends React.Component {
  componentDidUpdate (prevProps, prevState) {
    if (this.props.isSuccess) {
      this.props.resetCreateSurvey()
      this.props.router.push(Path.editSurvey(this.props.newSurvey))
    }
  }

  render () {
    return (
      <NewSurveyView
        isLoading={this.props.isLoading}
        onClick={() => this.props.createSurvey(this.props.currentUser.id)}
      />
    )
  }
}

const mapStateToProps = (state) => ({
  currentUser: state.session.user,
  newSurvey: state.createSurvey.survey,
  isLoading: state.createSurvey.isLoading,
  isSuccess: !!state.createSurvey.survey,
  error: state.createSurvey.error
})

const mapDispatchToProps = (dispatch) => {
  return {
    createSurvey: bindActionCreators(createSurveyRequest, dispatch),
    resetCreateSurvey: bindActionCreators(resetCreateSurvey, dispatch)
  }
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(NewSurvey))
