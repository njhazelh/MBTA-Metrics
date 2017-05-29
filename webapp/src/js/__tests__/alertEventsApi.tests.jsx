/* eslint-env jest */
import Moxios from 'moxios';

import * as alertEventsApi from '../api/alertEvents';

test('The API Works', () => {
  Moxios.withMock((done) => {
    alertEventsApi.getAlertEvents(
      '2017-04-26', '2017-04-27',
      '00:00:00', '23:59:59',
    );
    Moxios.wait(() => {
      const request = Moxios.requests.mostRecent();
      request.respondWith({
        status: 200,
        response: {
          data: [],
        },
      }).then(() => {
        done();
      });
    });
  });

  Moxios.withMock((done) => {
    alertEventsApi.getAlertEvents(
      '2017-04-26', '2017-04-27',
      '00:00:00', '23:59:59',
    );
    Moxios.wait(() => {
      const request = Moxios.requests.mostRecent();
      request.respondWith({
        status: 400,
        response: {
          data: [],
        },
      }).then(() => {
        done();
      });
    });
  });
});
