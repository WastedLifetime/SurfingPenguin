import React from 'react'
import PropTypes from 'prop-types'
import QuestionWrapper from './QuestionPreviewWrapper'

class QuestionList extends React.Component {
  render () {
    let { questionOrder, questions, currentQuestionID } = this.props
    let orderedQuestions = questionOrder.map(id => questions[id])
    return (
      <ul className='list-unstyled'>
        {orderedQuestions.map((question, index) => {
          return (
            <li key={question._id}>
              <QuestionWrapper
                question={question}
                showUp={index !== 0}
                showDown={index !== orderedQuestions.length - 1}
                isActive={currentQuestionID === question._id}
                onActive={() => this.props.onActive(question._id)}
                onRemove={() => this.props.onRemove(question)}
                onClone={() => this.props.onClone(question)}
                onUp={() => this.props.onUp(question)}
                onDown={() => this.props.onDown(question)}
              />
            </li>
          )
        })}
      </ul>
    )
  }
}

QuestionList.propTypes = {
  questions: PropTypes.object,
  questionOrder: PropTypes.array,
  active_question_id: PropTypes.string,
  onClone: PropTypes.func,
  onRemove: PropTypes.func,
  onSort: PropTypes.func,
  onActive: PropTypes.func
}

export default QuestionList
