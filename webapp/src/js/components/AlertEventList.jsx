import React from 'react';
import { connect } from 'react-redux';

import DateTimeSelector from './DateTimeSelector';
import AlertEvent from './AlertEvent';
import store from '../store';
import { loadActionEvents } from '../actions/alertEvent-actions';
import * as alertEventApi from '../api/alertEvents';

import { Container, Row, Col, Table } from 'reactstrap';

class AlertEventList extends React.Component {
  render() {
    const table = this.props.alertEvents.length === 0
      ? <tr style={{textAlign:'center'}}>
          <td colSpan='17' className='py-5'>No Data Loaded</td>
        </tr>
      : this.props.alertEvents.map(alertEvent =>
          <AlertEvent data={alertEvent} key={alertEvent.id}/>
        );

    return (
      <Table responsive striped bordered className='table-sm mt-5'>
        <thead className='thead-default'>
          <tr>
            <th>Trip ID</th>
            <th>Date</th>
            <th>Time</th>
            <th>Day</th>
            <th>Route</th>
            <th>Stop</th>
            <th>Direction</th>
            <th>Short Name</th>
            <th>Scheduled Dep.</th>
            <th>Actual Dep.</th>
            <th>Delay</th>
            <th>Alert?</th>
            <th>Deserves Alert?</th>
            <th>Alert Delay</th>
            <th>Alert Text</th>
            <th>Predicted Delay</th>
            <th>Delay Accuracy</th>
          </tr>
        </thead>
        <tbody>
          {table}
        </tbody>
      </Table>
    );
  }
}

const mapStateToProps = function(store) {
  return {
    alertEvents: store.alertEvents
  };
}

export default connect(mapStateToProps)(AlertEventList);
