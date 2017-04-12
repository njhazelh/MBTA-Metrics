import axios from 'axios';

import store from '../store';
import { getAlertEventsSuccess } from '../actions/alertEvent-actions'

export function getAlertEvents(startDate, endDate, startTime, endTime) {
  console.info(
    'Loading alert_events: dates(%s to %s), times(%s to %s)',
    startDate, endDate, startTime, endTime
  );
  return axios.get(
    '/data/alert_events', {
      params: {
        startDate: startDate,
        endDate: endDate,
        startTime: startTime,
        endTime: endTime,
      }
    }).then(response => {
      if (
        response == null
        || response.data == null
        || response.data.data == null
        || !Array.isArray(response.data.data)
      ) {
        console.error(
          'Received malformed alert_event data from API',
          response
        );
        return response;
      }
      console.info(
        'Received %d alert_events from API',
        response.data.data.length
      );
      store.dispatch(getAlertEventsSuccess(response.data.data));
      return response;
    }).catch(error => {
      console.error('API Error "alert_events":', error);
    });
}
