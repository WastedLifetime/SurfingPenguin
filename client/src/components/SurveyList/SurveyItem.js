import React from 'react'
import './SurveyItem.css'
import { withRouter, Link } from 'react-router'

class SurveyItem extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      hide: false
    }
  }

  render () {
    let { survey, location } = this.props
    return (
      <div className='SurveyItem'>
        <button onClick={() => this.showsurvey()} >{survey.surveyname}</button>
        <div>
          {this.showquestion()}
        </div>
      </div>

    )
  }
  showsurvey () {
    this.setState({
      hide: !this.state.hide
    })
  }
  showquestion () {
    if (this.state.hide) {
      return <div><ul className='list-unstyled'>
        {this.props.survey.questions.map(question => {
          return <li key={question.idx} className='col-md-3'>{question.title}</li>
        })}
        <Link to={`/surveys/${this.props.survey.id}/`}>{"Show detail"}</Link>
      </ul></div>
    }
  }
}

SurveyItem.propTypes = {}
SurveyItem.defaultProps = {}

export default SurveyItem
// {this.props.fetchSurvey(this.props.surveyId)}
