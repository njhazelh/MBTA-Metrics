import React from 'react';

class AlertEvent extends React.Component {
  render() {
    let ae = this.props.data;
    return (
      <tr>
        <td>{ae.date}</td>
        <td>{ae.route}</td>
        <td>{ae.direction}</td>
        <td>{ae.stop}</td>
        <td>{ae.scheduled_departure}</td>
        <td>{ae.actual_departure}</td>
        <td>{ae.delay}</td>
        <td>{ae.alert_issued ? 'Yes' : 'No'}</td>
        <td>{ae.alert_delay}</td>
        <td>{ae.alert_text}</td>
        <td>{ae.predicted_delay}</td>
      </tr>
    );
  }
}


export default AlertEvent;
