import React from 'react';

class AlertEvent extends React.Component {
  render() {
    let ae = this.props.data;
    return (
      <tr>
        <td>{ae.trip_id}</td>
        <td>{ae.date}</td>
        <td>{ae.time}</td>
        <td>{ae.day}</td>
        <td>{ae.route}</td>
        <td>{ae.stop}</td>
        <td>{ae.direction}</td>
        <td>{ae.short_name}</td>
        <td>{ae.scheduled_departure}</td>
        <td>{ae.actual_departure}</td>
        <td>{ae.delay}</td>
        <td>{ae.alert_issued ? 'Yes' : 'No'}</td>
        <td>{ae.deserves_alert ? 'Yes' : 'No'}</td>
        <td>{ae.alert_delay}</td>
        <td>{ae.alert_text}</td>
        <td>{ae.predicted_delay}</td>
        <td>{ae.delay_accuracy}</td>
      </tr>
    );
  }
}


export default AlertEvent;
