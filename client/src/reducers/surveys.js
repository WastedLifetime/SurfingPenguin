import { combineReducers } from 'redux'
export const FETCH_SURVEYS_REQUEST = 'FETCH_SURVEYS_REQUEST'

export const FETCH_SURVEYS_REQUEST_SUCCESS = 'FETCH_SURVEYS_REQUEST_SUCCESS'
export const FETCH_SURVEYS_REQUEST_FAIL = 'FETCH_SURVEY_SREQUEST_FAIL'

export const fetchReducer = (state = {surveys: [], isLoading: false, error: null}, action) => {
  switch (action.type) {
    case FETCH_SURVEYS_REQUEST:
      return {
        isLoading: true,
        error: null,
        surveys: []
      }
    case FETCH_SURVEYS_REQUEST_SUCCESS:
      return {
        isLoading: false,
        error: null,
        surveys: action.payload
      }
    case FETCH_SURVEYS_REQUEST_FAIL:
      return {
        isLoading: false,
        error: action.payload,
        surveys: []
      }
    case 'CREATE_SURVEY_REQUEST':
      return {
        ...state,
        isCreating: true,
        error: null
      }
    case 'CREATE_SURVEY_REQUEST_SUCCESS':
      return {
        ...state,
        isCreating: false,
        error: null
      }
    case 'CREATE_SURVEY_REQUEST_FAIL':
      return {
        ...state,
        isCreating: false,
        error: action.payload
      }
    default:
      console.log(action.type)
      return state
  }
}

export default combineReducers({
  fetchSurvey: fetchReducer,
})

export const getSurveys = (state) => state.fetchSurvey.surveys

export const getFetchStatus = (state) => {
  return state.fetchSurvey.isLoading
}

export const getFetchError = (state) => {
  return state.fetchSurvey.error
}
