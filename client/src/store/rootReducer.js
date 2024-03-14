import { combineReducers } from '@reduxjs/toolkit';
import configuration from './configuration.store'
import globalReducer from './global.store'
import userReducer from './user.store'

const rootReducer = combineReducers({
    configuration: configuration,
    global: globalReducer,
    user: userReducer
});

export default rootReducer;