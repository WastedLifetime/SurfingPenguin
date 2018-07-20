import React, { Component } from 'react'
import { connect } from 'react-redux'
import RegisterFormView from '../components/RegisterForm'
import {registerRequest, registerRequestSuccess, registerRequestFail, registerRequestFailDuplicateUsername} from '../actions/register'

class RegisterPage extends Component {
  componentWillReceiveProps (nextProps) {
    if (nextProps.isRegisterSuccess) {
      this.props.router.push('/login')
    }
  }

  render () {
    return (
      <div className='col-md-4 col-md-offset-4' style={{marginTop: '40px'}}>
        <RegisterFormView {...this.props} />
      </div>
    )
  }
}

const mapStateToProps = (state) => {
  return {
    isRegisterSuccess: state.register.isSuccess
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
    onSubmit: (values) => {
      return dispatch(registerRequest({
        username: values.username,
        password: values.password
      })).then(res => {
        if (res.messages === 'use another name') {
          dispatch(registerRequestFailDuplicateUsername(res))
          return Promise.reject(res)
        } else {
          dispatch(registerRequestSuccess(res))
          return Promise.resolve(res)
        }
      }).catch(err => {
        dispatch(registerRequestFail(err))
        return Promise.reject(err)
      })
    }
  }
}

let registerPage = connect(mapStateToProps, mapDispatchToProps)(RegisterPage)

export default registerPage
