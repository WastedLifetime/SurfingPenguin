import React from 'react'
import './SurveyItem.css'

class SurveyItem extends React.Component<Props> {
  constructor (props) {
    super(props)
    this.state = {
      hide: false
    }
  }

  render () {
    let { survey } = this.props
    console.log(survey)
    return (
      <a href='#' className='list-group-item list-group-item-action flex-column align-items-start'>
        <div className='d-flex w-100 justify-content-between'>
      <div className='SurveyItem'>
          <h5 className='mb-1'>標題</h5>
          <small>已截止</small>
        </div>

      </div>
        <p className='mb-1'>Donec id elit non mi porta gravida at eget metus. Maecenas sed diam eget risus varius blandit.</p>
        <button onClick={() => this.showsurvey()} >{survey.surveyname}</button>
        <div>
          {this.showquestion()}
        </div>
        <i className='fa fa-bookmark' aria-hidden='true'> 收藏</i>
        <i className='fa fa-pencil' aria-hidden='true'> 60</i>
      </a>

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
      </ul></div>
    }
  }
}

SurveyItem.propTypes = {}
SurveyItem.defaultProps = {}

export default SurveyItem
// {this.props.fetchSurvey(this.props.surveyId)}
