import React from 'react'
import { fetchSurvey } from '../../actions/editSurvey'
import { Link } from 'react-router'
import { Path } from '../../routes'
import './SurveyItem.css'

class SurveyItem extends React.Component {
  	constructor(props) {
    super(props);

    this.state = {
      hide: 0,
      message: "",
    };
  }  
   
  render () {
    let { survey, survey: { title } } = this.props
    return (
      <div className='SurveyItem'>
        <button onClick={() => this.showsurvey()} >{this.props.survey.surveyname}</button>
        <div>{this.state.message}</div>
        {this.showquestion()}
        
      </div>
      
    )
  }
  showsurvey() {
  	this.setState({
      hide : this.state.hide+1,
    });
    console.log(this.state.hide);
	}
  showquestion() {
    if(this.state.hide % 2 == 1)
      return <div><ul className='list-unstyled'>
          {this.props.survey.questions.map(question => {
            return <li key={question.idx} className='col-md-3'>{question.title}</li>
          })}
        </ul></div>;
  }
  
}

SurveyItem.propTypes = {}
SurveyItem.defaultProps = {}

export default SurveyItem
// {this.props.fetchSurvey(this.props.surveyId)}