/* eslint-env jest */

import React from 'react';
import { Provider } from 'react-redux';
import renderer from 'react-test-renderer';
import Moment from 'moment';

import AlertEventList from '../components/AlertEventList';
import store from '../store';
import { getAlertEventsSuccess } from '../actions/alertEvent-actions';
import * as filterActions from '../actions/filterActions';

test('AlertEventList should render data', () => {
  const component = renderer.create(
    <Provider store={store}><AlertEventList /></Provider>,
  );
  store.dispatch(filterActions.setAllDirectionFilters(true));
  store.dispatch(filterActions.setAllLineFilters(true));
  store.dispatch(filterActions.setAllAlertFilters(true));

  store.dispatch(getAlertEventsSuccess([
    { id: 1, direction: 'inbound' },
    { id: 2, direction: 'outbound', deserves_alert: true, alert_issued: true },
    { id: 3, direction: 'inbound', delay: -14.999, actual_departure: Moment('2017-04-26') },
    { id: 4, alert_delay: 5.1111, scheduled_departure: Moment('2017-04-26') },
    { id: 5, date: Moment('2017-04-26'), time: Moment('2017-04-26') },
  ]));
  expect(component.toJSON()).toMatchSnapshot();

  store.dispatch(filterActions.setDirectionFilter('inbound', false));
  store.dispatch(filterActions.setLineFilter('CR-Middleborough', false));
  store.dispatch(filterActions.setAlertFilter('accurate', false));
  expect(component.toJSON()).toMatchSnapshot();

  store.dispatch(filterActions.setAllDirectionFilters(false));
  store.dispatch(filterActions.setAllLineFilters(false));
  store.dispatch(filterActions.setAllAlertFilters(false));
  expect(component.toJSON()).toMatchSnapshot();
});
