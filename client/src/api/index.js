// import newId from '../util/idGenerator';
import axios from 'axios'
// import { hashHistory } from 'react-router';
// import decode from 'jwt-decode';

const fetcher = axios.create({
  baseURL: process.env.REACT_APP_ENDPOINT,
  headers: {
    'Content-Type': 'application/json',
    'Authorization': window.localStorage.session
  }
})

export const createUser = (params) => {
  return fetcher.post('/register', params).then(res => res.data)
}

export const login = (username, password) => {
  return fetcher.post('/login', {
    username,
    password
  }).then(res => {
    window.localStorage.session = res.data.messages
    fetcher.defaults.headers.common['Authorization'] = res.data.messages

    return res.data.messages
  })
}

export const logout = () => {
  delete window.localStorage.session
  return Promise.resolve()
}

export const fetchCurrentUser = () => {
  return fetcher.get('/users/me').then(res => {
    return res.data
  })
}

export const fetchUserSurveys = (user) => {
  return fetcher.get(`/show_all_surveys`).then(res => res.data)
}

export const fetchResults = (surveyId) => {
  return fetcher.get(`/surveys/${surveyId}/results`).then(res => res.data)
}

export const createSurvey = (userId, initSurvey) => {
  return fetcher.post(`create_survey`, initSurvey).then(res => res.data)
}

export const saveResult = (surveyId, result) => {
  return fetcher.post(`/surveys/${surveyId}/results`, result)
}

export const fetchSurvey = (surveyId) => {
  return fetcher.post(`/search_survey_by_id`, {id: surveyId}).then(res => (res.data))
}

export const deleteSurvey = surveyId => {}

export const updateSurvey = (survey) => {
  return fetcher.put(`/surveys/${survey.id}`, survey).then(res => res.data)
}

export const deleteResults = (surveyId, results) => {
  return Promise.all(results.map(result => fetcher.delete(`/surveys/${surveyId}/results/${result.id}`)))
}
