import * as api from '../api'
import { fetchSurveysRequest } from './surveys'

export const loginRequest = (username, password) => dispatch => {
  dispatch({
    type: 'LOGIN_REQUEST',
    payload: {
      username,
      password
    }

  })
  return api.login(username, password)
}

export const loginRequestSuccess = (res) => (dispatch) => {
  dispatch({
    type: 'LOGIN_REQUEST_SUCCESS',
    payload: res
  })
  dispatch(fetchSurveysRequest(res))
}

export const loginRequestFail = (err) => ({
  type: 'LOGIN_REQUEST_FAIL',
  payload: err
})
export const loginRequestFailUserNotFound = (err) => ({
  type: 'LOGIN_REQUEST_FAIL_USER_NOT_FOUND',
  payload: err
})
export const loginRequestFailWrongPasswd = (err) => ({
  type: 'LOGIN_REQUEST_FAIL_WRONG_PASSWD',
  payload: err
})

export const fetchCurrentUserRequest = () => dispatch => {
  dispatch({
    type: 'CURRENT_USER_REQUEST'
  })
  return api.fetchCurrentUser()
}

export const fetchCurrentUserRequestSuccess = (res) => ({
  type: 'CURRENT_USER_REQUEST_SUCCESS',
  payload: res
})

export const fetchCurrentUserRequestFail = (prevPath) => ({
  type: 'CURRENT_USER_REQUEST_FAIL',
  payload: prevPath
})
