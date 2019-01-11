import React, { Component } from 'react'
import { connect } from 'react-redux'
import SurveyItem from '../components/SurveyList/SurveyItem'
import SurveyList from '../components/SurveyList/SurveyList'
import { bindActionCreators } from 'redux'
import { getSurveys, getFetchError, getFetchStatus, getSubmitStatus } from '../reducers/surveys'
import '../css/search.css'
// import '../css/bootstrap.css'
import '../css/font-awesome/css/font-awesome.min.css'
import { fetchSurveysRequest } from '../actions/surveys'

class SurveyListPage extends Component {
  render () {
    console.log(this.props.surveys)
    console.log(this.props.surveys.length)
    return (
      <div className='SurveyList'>
        <div id='sidebar'>
          <ul>
            <li><a href='#'>我的問卷</a> </li>
            <li><a href='#'>我的獎品</a> </li>
            <li><a href='#'>共用問卷</a> </li>
            <li><a href='#'>追蹤問卷</a> </li>
          </ul>
        </div>
        <div id='search'>

          <form className='form-inline'>

            <input className='form-control mr-sm-2' type='search' placeholder='關鍵字' aria-label='Search' />
            <i className='fa fa-search fa-2x' aria-hidden='true' />
          </form>
        </div>

        <div id='select'>
          <ul>
            <li><a href='#'>最新問卷</a> </li>
            <li><a href='#'>熱門問卷</a> </li>
            <li><a href='#'>已截止</a> </li>
            <li>
              <button type='button' className='create_btn'><i className='fa fa-pencil' aria-hidden='true'> 建問卷</i></button>
            </li>
          </ul>
        </div>
        <div id='content'>
          <div className='list-group'>
            <SurveyList {...this.props.surveys}>
            </SurveyList>
          </div>
        </div>
      </div>
    )
  }
}
const mapStateToProps = (state, { params }) => {
  console.log(state)
  return {
    surveys: getSurveys(state.surveys),
    isLoading: getFetchStatus(state.surveys),
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
    fetchSurveys: bindActionCreators(fetchSurveysRequest(), dispatch),
      dispatch,
  }
}
export default connect(mapStateToProps)(SurveyListPage)
