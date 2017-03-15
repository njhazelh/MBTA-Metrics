import React from 'react';
import ReactDOM from 'react-dom';

import {
    Router,
    Route,
    Link,
    IndexRoute,
    hashHistory,
} from 'react-router';

class WebApp extends React.Component {
    render() {
        return (<div className="app">
          <h1>MBTA Alert Metrics</h1>
          <Link to="/">Home</Link>
          <Link to="/test">Test</Link>
          { this.props.children }
        </div>);
    }
}


WebApp.propTypes = {
    children: React.PropTypes.node,
};

WebApp.defaultProps = {
    children: [],
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
