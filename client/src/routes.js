import React from 'react'
import { Route, IndexRoute } from 'react-router'
import App from './App'
import Home from './pages/HomePage'
import SurveyListPage from './pages/SurveyListPage'
import RegisterPage from './pages/RegisterPage'
import LoginPage from './pages/LoginPage'
import LogoutPage from './pages/LogoutPage'
import UserSurveyPage from './pages/UserSurveyPage'
import NewSurveyPage from './pages/NewSurveyPage'
import SharedSurveyPage from './pages/SharedSurveyPage'
import CollectedSurveyPage from './pages/CollectedSurveyPage'
import SettingPage from './pages/SettingPage'
import PrivacyPage from './pages/PrivacyPage'
import ContactPage from './pages/ContactPage'
import SupportPage from './pages/SupportPage'
import DonatePage from './pages/DonatePage'
import EditSurveyPage from './pages/EditSurveyPage'
import SurveyDataPage from './pages/SurveyDataPage'
import OverviewSurveyPage from './pages/OverviewSurveyPage'
import SurveyReportPage from './pages/SurveyReportPage'
import SurveyPage from './pages/SurveyPage'

import { fetchCurrentUserRequest, fetchCurrentUserRequestSuccess, fetchCurrentUserRequestFail } from './actions/login'
import { home } from './reducers/session'

const skipAuthPaths = ['/login', '/register', '/logout']

export default function routes (store) {
  function requireAuth (nextState, replace, next) {
    const state = store.getState()
    const nextPath = nextState.location.pathname
    console.log(nextPath)
    if (!state.session.user && skipAuthPaths.indexOf(nextPath) === -1) {
      store.dispatch(fetchCurrentUserRequest()).then(res => {
        store.dispatch(fetchCurrentUserRequestSuccess(res))
        dispatchHomePage(nextState, replace, store)
        next()
      }).catch(
        store.dispatch(fetchCurrentUserRequestFail(nextPath)),
        replace('/login'),
        next()
      )
    } else {
      dispatchHomePage(nextState, replace, store)
      next()
    }
  }

  function dispatchHomePage (nextState, replace, store) {
    const state = store.getState()
    if (state.session.user && nextState.location.pathname === '/') {
      replace({
        pathname: home(state.session.user)
      })
    }
  }

  return (
    // TODO: fix authentication
    <Route path='/' component={App}>
      <IndexRoute component={Home} />
      <Route path='register' component={RegisterPage} />
      <Route path='login' component={LoginPage} />
      <Route path='surveys' component={SurveyListPage} />
      <Route path='logout' component={LogoutPage} />
      <Route path='user/my_surveys' component={UserSurveyPage} />
      <Route path='user/shared_surveys' component={SharedSurveyPage} />
      <Route path='user/collected_surveys' component={CollectedSurveyPage} />
      <Route path='create_survey' component={NewSurveyPage} />
      <Route path='support' component={SupportPage} />
      <Route path='privacy' component={PrivacyPage} />
      <Route path='contact_us' component={ContactPage} />
      <Route path='donate' component={DonatePage} />
      <Route path='user/settings' component={SettingPage} />
      <Route path='surveys/:surveyId' component={SurveyPage} />
    </Route>
  )
}

export const Path = {
  survey (survey) {
    return `/user/surveys/${survey.id}/`
  },

  editSurvey (survey) {
    return `/user/surveys/${survey.id}/edit`
  },

  surveyList () {
    return `/user/surveys`
  },

  viewSurvey (survey) {
    return `/surveys/${survey.id}`
  },

  login () {
    return `/login`
  },

  logout () {
    return `/logout`
  }
}
