import axios from 'axios';

import store from '../store';
import { getAlertEventsSuccess } from '../actions/alertEvent-actions'

export function getAlertEvents() {
  return axios.get("/data/alert_events")
    .then(response => {
      store.dispatch(getAlertEventsSuccess(response.data));
      return response;
    });
}
