import React from 'react';
import { Router, Route, IndexRoute, hashHistory} from 'react-router';

import Home from './components/Home';
import AlertEventList from './components/AlertEventList';

const Hello = () =>
  <section>
    <h1>
      Welcome to the MTBA Alert Metrics page.
    </h1>
    <div className='lead'>
      <p>
        This site is intended to provide
        insight into the accuracy and existence of MBTA alerts related to the
        commuter rail.
      </p>
      <p>
        Since this page is a work in progress, don't expect everything to work,
        but check-back soon, and hopefully things will be better.
      </p>
    </div>
  </section>;

export default (
  <Router history={hashHistory}>
    <Route path="/" component={Home}>
      <IndexRoute component={Hello} />
      <Route path="list" component={AlertEventList} />
    </Route>
  </Router>
);
