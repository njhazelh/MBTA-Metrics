import React from 'react';
import { connect } from 'react-redux';
import { Table } from 'reactstrap';

import AlertEvent from './AlertEvent';


class AlertEventList extends React.Component {
  render() {
    const { alertEvents } = this.props;
    const table = alertEvents.length === 0
      ? (<tr style={{ textAlign: 'center' }}>
        <td colSpan="17" className="py-5">No Data Loaded</td>
      </tr>)
      : alertEvents.map(alertEvent =>
        <AlertEvent data={alertEvent} key={alertEvent.id} />,
        );

    return (
      <Table responsive striped bordered className="table-sm mt-2">
        <thead className="thead-default">
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

export default connect(data => ({ alertEvents: data.alertFilteredData }))(AlertEventList);
