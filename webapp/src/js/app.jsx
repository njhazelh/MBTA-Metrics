import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';

import router from './router.jsx';
import store from './store.jsx';

// This acts as a mock API when built using the dev environment script
// otherwise it should be an empty module
import 'alert_events_api';

ReactDOM.render(
  <Provider store={store}>{router}</Provider>,
  document.getElementById('root')
);
