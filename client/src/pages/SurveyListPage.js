import React, { Component } from 'react'
import '../css/search.css'
// import '../css/bootstrap.css'
import '../css/font-awesome/css/font-awesome.min.css'

class SurveyList extends Component {
  render () {
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

            <a href='#' className='list-group-item list-group-item-action flex-column align-items-start'>
              <div className='d-flex w-100 justify-content-between'>
                <h5 className='mb-1'>標題</h5>
                <small>已截止</small>
              </div>
              <p className='mb-1'>Donec id elit non mi porta gravida at eget metus. Maecenas sed diam eget risus varius blandit.</p>
              <i className='fa fa-bookmark' aria-hidden='true'> 收藏</i>
              <i className='fa fa-pencil' aria-hidden='true'> 60</i>
            </a>

            <a href='#' className='list-group-item list-group-item-action flex-column align-items-start'>
              <div className='d-flex w-100 justify-content-between'>
                <h5 className='mb-1'>標題</h5>
                <small>進行中</small>
              </div>
              <p className='mb-1'>Donec id elit non mi porta gravida at eget metus. Maecenas sed diam eget risus varius blandit.</p>
              <i className='fa fa-bookmark' aria-hidden='true'>收藏</i>
              <i className='fa fa-pencil' aria-hidden='true'> 50</i>
            </a>

            <a href='#' className='list-group-item list-group-item-action flex-column align-items-start'>
              <div className='d-flex w-100 justify-content-between'>
                <h5 className='mb-1'>標題</h5>
                <small>已截止</small>
              </div>
              <p className='mb-1'>Donec id elit non mi porta gravida at eget metus. Maecenas sed diam eget risus varius blandit.</p>
              <i className='fa fa-bookmark' aria-hidden='true'>收藏</i>
              <i className='fa fa-pencil' aria-hidden='true'> 100</i>
            </a>
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

export default SurveyList
