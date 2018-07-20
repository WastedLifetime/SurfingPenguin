import EditQuestionPanelView from '../components/EditPanel/EditQuestionPanel'
import { connect } from 'react-redux'
import { updateQuestion } from '../actions/editSurvey'
import { getActiveQuestion } from '../reducers/editSurvey'

const mapStateToProps = (state) => {
  return {
    question: getActiveQuestion(state.editSurvey)
  }
}

const mapDispatchToProps = {
  updateQuestion
}

const EditQuestionPanel = connect(
  mapStateToProps,
  mapDispatchToProps
)(EditQuestionPanelView)

export default EditQuestionPanel
