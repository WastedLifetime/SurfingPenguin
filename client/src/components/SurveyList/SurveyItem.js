import React from 'react';
import PropTypes from 'prop-types';
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import Typography from '@material-ui/core/Typography';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import './SurveyItem.css'
import { withRouter, Link } from 'react-router'

class SurveyItem extends React.Component<Props> {
  constructor (props) {
    super(props)
    this.state = {
      hide: false
    }
  }
    getQuestions() {
        if (this.props.questions) {
            return Object.keys(this.props.questions).map( (question) => {
                return Object.keys(this.props.questions[question]).map( (key) => {
                    return <div>{key}: {this.props.questions[question][key]}</div>;
            })});
        } else {
            return <p>data is not available</p>;
        }
    }


  // TODO: render questions
  render () {
    let survey = this.props
    let questions = survey.questions
    console.log(questions)
    return (
        <a href='#' className='list-group-item list-group-item-action flex-column align-items-start'>
          <div className='d-flex w-100 justify-content-between'>
            <h5 className='mb-1'>{survey.surveyname}</h5>
            <small>已截止</small>
          </div>
          <div>{this.getQuestions()}</div>
          <p className='mb-1'>Donec id elit non mi porta gravida at eget metus. Maecenas sed diam eget risus varius blandit.</p>
          <i className='fa fa-bookmark' aria-hidden='true'>收藏</i>
          <i className='fa fa-pencil' aria-hidden='true'> 20</i>
        </a>
    )
  }
  showsurvey () {
    this.setState({
      hide: !this.state.hide
    })
  }
  showquestion () {
    // TODO: Pass props (survey) through link
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
