import Moment from 'moment';

import {
  FROM_DATE, TO_DATE, FROM_TIME, TO_TIME,
  DIRECTIONS, LINE_VALUES, ALERTS,
} from '../constants';

import * as types from '../actions/action-types';

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

export default function reducer(state = initialState, action) {
  switch (action.type) {
  case types.LOAD_ALERT_EVENTS_SUCCESS:
    return {
      ...state,
      alertEvents: action.alertEvents.map(item => ({
        ...item,
        date: item.date && Moment(item.date),
        time: item.time && Moment(item.time, 'HH:mm:ss'),
        scheduled_departure: item.scheduled_departure && Moment(item.scheduled_departure, 'HH:mm:ss'),
        actual_departure: item.actual_departure && Moment(item.actual_departure, 'HH:mm:ss'),
      })),
    };
  case types.SET_DIRECTION_FILTER:
    return {
      ...state,
      directionFilters: {
        ...state.directionFilters,
        [action.direction]: action.value,
      },
    };
  case types.SET_ALL_DIRECTION_FILTERS: {
    const directionFilters = {};
    DIRECTIONS.forEach((d) => { directionFilters[d] = action.value; });
    return {
      ...state,
      directionFilters,
    };
  }
  case types.SET_LINE_FILTER:
    return {
      ...state,
      lineFilters: {
        ...state.lineFilters,
        [action.line]: action.value,
      },
    };
  case types.SET_ALL_LINE_FILTERS: {
    const lineFilters = {};
    LINE_VALUES.forEach((d) => { lineFilters[d] = action.value; });
    return {
      ...state,
      lineFilters,
    };
  }
  case types.SET_ALERT_FILTER:
    return {
      ...state,
      alertFilters: {
        ...state.alertFilters,
        [action.alert]: action.value,
      },
    };
  case types.SET_ALL_ALERT_FILTERS: {
    const alertFilters = {};
    ALERTS.forEach((d) => { alertFilters[d] = action.value; });
    return {
      ...state,
      alertFilters,
    };
  }
  case types.SET_DATETIME_FILTER:
    return {
      ...state,
      dateTimeFilters: {
        ...state.dateTimeFilters,
        [action.aspect]: action.value,
      },
    };
  default:
    return state;
  }
}
