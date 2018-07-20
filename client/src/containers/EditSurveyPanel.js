import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import EditSurveyPanelView from '../components/EditPanel/EditSurveyPanel'
import { getSurvey } from '../reducers/editSurvey'
import { updateSurveyHeader } from '../actions/editSurvey'

const mapStateToProps = (state) => {
  return {
    title: getSurvey(state.editSurvey).title,
    subTitle: getSurvey(state.editSurvey).subTitle
  }
}

const mapDispatchToProps = dispatch => {
  return {
    onUpdate: bindActionCreators(updateSurveyHeader, dispatch)
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(EditSurveyPanelView)
