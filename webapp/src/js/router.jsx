import React from 'react';
import { Router, Route, IndexRoute, hashHistory } from 'react-router';

import Home from './components/Home';
import Info from './components/InfoPage';
import MetricsPage from './components/MetricsPage';

export default (
  <Router history={hashHistory}>
    <Route path="/" component={Home}>
      <IndexRoute component={MetricsPage} />
      <Route path="info" component={Info} />
    </Route>
  </Router>
);
