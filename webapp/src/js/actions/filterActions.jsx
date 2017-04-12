import * as types from '../actions/action-types';

export function setDirectionFilter(direction, value) {
  return {
    type: types.SET_DIRECTION_FILTER,
    direction,
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

export function setAlertFilter(alert, value) {
  return {
    type: types.SET_ALERT_FILTER,
    alert,
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
