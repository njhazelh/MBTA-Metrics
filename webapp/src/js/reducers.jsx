import Moment from 'moment';

import { FROM_DATE, TO_DATE, FROM_TIME, TO_TIME } from './constants';
import * as types from './actions/action-types';

const initialState = {
  alertEvents: [],
  directionFilters: {},
  lineFilters: {},
  alertFilters: {},
  dateTimeFilters: {
    [FROM_DATE]: Moment().subtract({ days: 7 }).format('YYYY-MM-DD'),
    [TO_DATE]: Moment().format('YYYY-MM-DD'),
    [FROM_TIME]: '00:00',
    [TO_TIME]: '23:59',
  },
};

function setAlertEvents(state, action) {
  return {
    ...state,
    alertEvents: action.alertEvents,
  };
}

function setDirectionFilter(state, action) {
  return {
    ...state,
    directionFilters: {
      ...state.directionFilters,
      [action.direction]: action.value,
    },
  };
}

function setLineFilter(state, action) {
  return {
    ...state,
    lineFilters: {
      ...state.lineFilters,
      [action.line]: action.value,
    },
  };
}

function setAlertFilter(state, action) {
  return {
    ...state,
    alertFilters: {
      ...state.alertFilters,
      [action.alert]: action.value,
    },
  };
}

function setDateTimeFilter(state, action) {
  return {
    ...state,
    dateTimeFilters: {
      ...state.dateTimeFilters,
      [action.aspect]: action.value,
    },
  };
}

export default function reducer(state = initialState, action) {
  switch (action.type) {
  case types.LOAD_ALERT_EVENTS_SUCCESS:
    return setAlertEvents(state, action);
  case types.SET_DIRECTION_FILTER:
    return setDirectionFilter(state, action);
  case types.SET_LINE_FILTER:
    return setLineFilter(state, action);
  case types.SET_ALERT_FILTER:
    return setAlertFilter(state, action);
  case types.SET_DATETIME_FILTER:
    return setDateTimeFilter(state, action);
  default:
    return state;
  }
}
