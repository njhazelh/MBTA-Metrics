import React from 'react';
import { connect } from 'react-redux';

import AlertEvent from './AlertEvent';
import store from '../store';
import { loadActionEvents } from '../actions/alertEvent-actions';
import * as alertEventApi from '../api/alertEvents';

class AlertEventList extends React.Component {
  componentDidMount() {
    this.reload();
  }

  reload() {
    console.log('reloading');
    alertEventApi.getAlertEvents();
  }

  render() {
    if (this.props.alertEvents.length == 0) {
      return <span>Loading</span>;
    }

    let alertEvents = this.props.alertEvents.map(
      alertEvent => <AlertEvent data={alertEvent} key={alertEvent.id}/>
    );

    return (
      <div>
        <button onClick={this.reload}>Reload</button>
        <table className="table table-striped">
          <thead>
            <tr>
              <th>Date</th>
              <th>Route</th>
              <th>Direction</th>
              <th>Stop</th>
              <th>Scheduled Dep.</th>
              <th>Actual Dep.</th>
              <th>Delay</th>
              <th>Alert</th>
              <th>Alert Delay</th>
              <th>Alert Text</th>
              <th>Predicted Delay</th>
            </tr>
          </thead>
          <tbody>{alertEvents}</tbody>
        </table>
      </div>
    );

  }
}

const mapStateToProps = function(store) {
  return {
    alertEvents: store.alertEvents
  };
}

export default connect(mapStateToProps)(AlertEventList);
