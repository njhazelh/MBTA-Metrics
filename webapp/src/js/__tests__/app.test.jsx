/* eslint-env jest */

import React from 'react';
import { Provider } from 'react-redux';
import renderer from 'react-test-renderer';

import router from '../router';
import store from '../store';

test('The app renders', () => {
  const component = renderer.create(
    <Provider store={store}>{router}</Provider>,
  );
  expect(component.toJSON()).toMatchSnapshot();
});
