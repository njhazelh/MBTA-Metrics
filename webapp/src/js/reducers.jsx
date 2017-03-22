import * as types from './actions/action-types';


const initialState = {
  alertEvents: [],
};

function reducer(state = initialState, action) {
  switch (action.type) {
    case types.LOAD_ALERT_EVENTS_SUCCESS:
      return Object.assign({}, state, { alertEvents: action.alertEvents });
    default:
      return state;
  }
}

export default reducer;
