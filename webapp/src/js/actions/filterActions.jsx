import * as types from '../actions/action-types';

export function setDirectionFilter(direction, value) {
  return {
    type: types.SET_DIRECTION_FILTER,
    direction,
    value,
  };
}

export function setAllDirectionFilters(value) {
  return {
    type: types.SET_ALL_DIRECTION_FILTERS,
    value,
  };
}

export function setLineFilter(line, value) {
  return {
    type: types.SET_LINE_FILTER,
    line,
    value,
  };
}

export function setAllLineFilters(value) {
  return {
    type: types.SET_ALL_LINE_FILTERS,
    value,
  };
}


export function setAlertFilter(alert, value) {
  return {
    type: types.SET_ALERT_FILTER,
    alert,
    value,
  };
}

export function setAllAlertFilters(value) {
  return {
    type: types.SET_ALL_ALERT_FILTERS,
    value,
  };
}


export function setDateTimeFilter(aspect, value) {
  return {
    type: types.SET_DATETIME_FILTER,
    aspect,
    value,
  };
}
