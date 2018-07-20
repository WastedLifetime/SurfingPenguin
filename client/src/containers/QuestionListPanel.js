import { connect } from 'react-redux'
import QuestionListPanelView from '../components/EditPanel/QuestionListPanel'
import { addQuestion } from '../actions/editSurvey'
import { QuestionDescriptions } from '../constants/Questions'

export default connect(() => {
  return {
    questions: QuestionDescriptions.map(q => {
      return {
        text: q.text,
        action: () => addQuestion(q.type)
      }
    })
  }
})(QuestionListPanelView)
