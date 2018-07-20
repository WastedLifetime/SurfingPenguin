import { combineReducers } from 'redux'

import register from './register'
import session from './session'
import surveys from './surveys'
import createSurvey from './createSurvey'
import editSurvey from './editSurvey'
import survey from './survey'
import data from './data/index'

const root = combineReducers({
  register,
  session,
  surveys,
  createSurvey,
  editSurvey,
  survey,
  data
})

export default root
