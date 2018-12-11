import React, { Component } from 'react'
import { connect } from 'react-redux'
import SurveyItem from '../components/SurveyList/SurveyItem'
import { bindActionCreators } from 'redux'
import { getSurveys, getFetchError, getFetchStatus, getSubmitStatus } from '../reducers/surveys'
import '../css/search.css'
// import '../css/bootstrap.css'
import '../css/font-awesome/css/font-awesome.min.css'
import { fetchSurveysRequest } from '../actions/surveys'

class SurveyList extends Component {
  loaddata () {
    this.props.fetchsurvey()
  }

  componentdidmount () {
    this.getSurveys()
  }
  getSurveys() {
    fetch('http:/localhost:5000/api/0.1/show_all_surveys')
      .then(({ results }) => this.setState({ surveys: results }));
  }

  componentdidupdate (prevprops) {
    this.loaddata()
  }

  render () {
    console.log(this.props)
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
            <SurveyItem {...this.props}>
            </SurveyItem>

            <a href='#' className='list-group-item list-group-item-action flex-column align-items-start'>
              <div className='d-flex w-100 justify-content-between'>
                <h5 className='mb-1'>標題</h5>
                <small>已截止</small>
              </div>
              <p className='mb-1'>Donec id elit non mi porta gravida at eget metus. Maecenas sed diam eget risus varius blandit.</p>
              <i className='fa fa-bookmark' aria-hidden='true'>收藏</i>
              <i className='fa fa-pencil' aria-hidden='true'> 20</i>
            </a>
          </div>
        </div>
      </div>
    )
  }
}
const mapStateToProps = (state, { params }) => {
  return {
    survey: getSurveys(state.surveys),
    isLoading: getFetchStatus(state.surveys),
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
    fetchSurveys: bindActionCreators(fetchSurveysRequest, dispatch)
  }
}
export default connect(mapStateToProps, mapDispatchToProps)(SurveyList)
