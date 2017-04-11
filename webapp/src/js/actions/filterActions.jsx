import * as types from '../actions/action-types';

export function setDirectionFilter(direction, value) {
  return {
    type: types.SET_DIRECTION_FILTER,
    direction: direction,
    value: value,
  }
}

export function setLineFilter(line, value) {
  return {
    type: types.SET_LINE_FILTER,
    line: line,
    value: value,
  }
}

export function setAlertFilter(alert, value) {
  return {
    type: types.SET_ALERT_FILTER,
    alert: alert,
    value: value,
  }
}

export function setDateTimeFilter(aspect, value) {
  return {
    type: types.SET_DATETIME_FILTER,
    aspect: aspect,
    value: value,
  }
}
