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

  render () {
    let { survey, location } = this.props
    return (
      <ExpansionPanel>
        <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
          <Typography className="SimpleExpansionPanel-heading-2">{this.props.surveyname}</Typography>
        </ExpansionPanelSummary>
        <ExpansionPanelDetails>
          <Typography>
            Survey content
          </Typography>
        </ExpansionPanelDetails>
      </ExpansionPanel>
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
