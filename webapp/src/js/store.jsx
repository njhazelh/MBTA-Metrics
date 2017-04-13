import { createStore } from 'redux';
import reduceReducers from 'reduce-reducers';
import FilterDataReducer from './reducers/FilterDataReducer';
import ActionReducer from './reducers/ActionReducer';

const reducer = reduceReducers(ActionReducer, FilterDataReducer);
const store = createStore(reducer);
export default store;
