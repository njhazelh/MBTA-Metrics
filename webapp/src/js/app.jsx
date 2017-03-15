import React from 'react';
import ReactDOM from 'react-dom';

import {
    Router,
    Route,
    Link,
    IndexRoute,
    hashHistory,
} from 'react-router';

const WebApp = () => {
    const { children } = this.props;
    return (
      <div className="app">
        <h1>MBTA Alert Metrics</h1>
        <Link to="/">Home</Link>
        <Link to="/test">Test</Link>
        { children }
      </div>
    );
};

const Hello = () => <p>Hello World</p>;

const Test = () =>
  <table className="table table-striped">
    <thead>
      <tr>
        <th>#</th>
        <th>X</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>1</td>
        <td>asdf</td>
      </tr>
      <tr>
        <td>2</td>
        <td>hjkl</td>
      </tr>
    </tbody>
  </table>;

ReactDOM.render(
  <Router history={hashHistory}>
    <Route path="/" component={WebApp}>
      <IndexRoute component={Hello} />
      <Route path="test" component={Test} />
    </Route>
  </Router>,
    document.getElementById('app'),
);
