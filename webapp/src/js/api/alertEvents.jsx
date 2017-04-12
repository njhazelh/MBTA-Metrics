import axios from 'axios';

import store from '../store';
import { getAlertEventsSuccess } from '../actions/alertEvent-actions'

export function getAlertEvents(startDate, endDate, startTime, endTime) {
  console.info(
    'Loading alert_events: dates(%s to %s), times(%s to %s)',
    startDate, endDate, startTime, endTime
  );
  return axios.get(
    "/data/alert_events", {
      params: {
        startDate: startDate,
        endDate: endDate,
        startTime: startTime,
        endTime: endTime,
      }
    }).then(response => {
      console.info('Received alert_events');
      store.dispatch(getAlertEventsSuccess(response.data));
      return response;
    }).catch(error => {
      console.error('API Error "alert_events":', error);
    });
}
