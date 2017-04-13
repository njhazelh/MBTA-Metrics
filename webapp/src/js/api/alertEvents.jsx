import axios from 'axios';

import store from '../store';
import { getAlertEventsSuccess } from '../actions/alertEvent-actions';

export async function getAlertEvents(startDate, endDate, startTime, endTime) {
  console.info(
    'Loading alert_events: dates(%s to %s), times(%s to %s)',
    startDate, endDate, startTime, endTime,
  );
  try {
    const response = await axios.get('/data/alert_events', {
      params: {
        startDate,
        endDate,
        startTime: `${startTime}:00`,
        endTime: `${endTime}:00`,
      },
    });
    console.info(
      'Received %d alert_events from API',
      response.data.data.length,
    );
    store.dispatch(getAlertEventsSuccess(response.data.data));
  } catch (error) {
    console.error('API Error "alert_events":', error.message);
  }
}
