import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';

// This acts as a mock API when built using the dev environment script
// otherwise it should be an empty module
/*
  eslint-disable
    import/no-unresolved,
    import/no-extraneous-dependencies,
    import/extensions
*/
import 'alert_events_api';
/*
  eslint-enable
    import/no-unresolved,
    import/no-extraneous-dependencies,
    import/extensions
*/

import router from './router';
import store from './store';

ReactDOM.render(
  <Provider store={store}>{router}</Provider>,
  document.getElementById('root'),
);
