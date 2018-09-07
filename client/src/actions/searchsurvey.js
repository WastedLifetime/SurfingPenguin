import * as api from '../api'

export const searchsurveyRequest = (surveyID) => dispatch => {
  dispatch({
    type: 'SEARCH_SURVEY_REQUEST',
    surveyID
  })
  return api.fetchSurvey(surveyID)
}

export const searchsurveyRequestSuccess = (res) => ({
  type: 'SEARCH_SURVEY_REQUEST_SUCCESS',
  res
})

export const searchsurveyRequestFail = (err) => ({
  type: 'LOGIN_REQUEST_FAIL',
  err
})
