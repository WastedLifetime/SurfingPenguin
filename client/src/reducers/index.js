import { combineReducers } from 'redux'

import register from './register'
import session from './session'
import surveys from './surveys'
import createSurvey from './create_survey'
import editSurvey from './edit_survey'
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
