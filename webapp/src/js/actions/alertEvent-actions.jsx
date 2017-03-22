import * as types from '../actions/action-types';

export function getAlertEventsSuccess(data) {
  return {
    type: types.LOAD_ALERT_EVENTS_SUCCESS,
    alertEvents: data
  }
}
