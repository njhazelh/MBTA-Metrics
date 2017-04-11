import axios from 'axios';

import store from '../store';
import { getAlertEventsSuccess } from '../actions/alertEvent-actions'

export function getAlertEvents(dateStart, dateEnd, timeStart, timeEnd) {
  console.info(
    'Loading alert_events: dates(%s to %s), times(%s to %s)',
    dateStart, dateEnd, timeStart, timeEnd
  );
  return axios.get(
    "/data/alert_events", {
      params: {
        dateState: dateStart,
        dateEnd: dateEnd,
        timeStart: timeStart,
        timeEnd: timeEnd,
      }
    }).then(response => {
      console.info('Received alert_events');
      store.dispatch(getAlertEventsSuccess(response.data));
      return response;
    }).catch(error => {
      console.error('API Error "alert_events":', error);
    });
}
