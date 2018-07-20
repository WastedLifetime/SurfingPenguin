import React from 'react'
import { withRouter } from 'react-router'
import { connect } from 'react-redux'
import EditFooterView from '../components/EditPanel/EditFooter'
import { bindActionCreators } from 'redux'
import {deleteSurvey, updateSurvey} from '../actions/editSurvey'
import { assembleSurvey, getSurvey } from '../reducers/editSurvey'
import { Path } from '../routes'
/* resetDeleteState */
class EditFooter extends React.Component {
  componentWillUnmount () {
    this.props.resetDeleteState()
  }

  componentWillReceiveProps (nextProps) {
    if (nextProps.isDeleteSuccess) {
      this.props.push(Path.surveyList())
    }
  }

  render () {
    return <EditFooterView {...this.props} />
  }
}

const mapStateToProps = (state, { router }) => {
  return {
    survey: assembleSurvey(getSurvey(state.editSurvey)),
    isDeleteSuccess: state.editSurvey.deleteSurvey.isSuccess,
    isUpdateSuccess: state.editSurvey.updateSurvey.isSuccess,
    push: router.push
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
    onDelete: bindActionCreators(deleteSurvey, dispatch),
    onSave: bindActionCreators(updateSurvey, dispatch),
    resetDeleteState: () => dispatch({
      type: 'RESET_DELETE_SURVEY_REQUEST'
    })
  }
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(EditFooter))
