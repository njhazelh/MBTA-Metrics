import React from 'react';

class AlertEvent extends React.Component {
  render() {
    const { data } = this.props;
    return (
      <tr>
        <td>{data.trip_id}</td>
        <td>{data.date}</td>
        <td>{data.time}</td>
        <td>{data.day}</td>
        <td>{data.route}</td>
        <td>{data.stop}</td>
        <td>{data.direction}</td>
        <td>{data.short_name}</td>
        <td>{data.scheduled_departure}</td>
        <td>{data.actual_departure}</td>
        <td>{data.delay}</td>
        <td>{data.alert_issued ? 'Yes' : 'No'}</td>
        <td>{data.deserves_alert ? 'Yes' : 'No'}</td>
        <td>{data.alert_delay}</td>
        <td>{data.alert_text}</td>
        <td>{data.predicted_delay}</td>
        <td>{data.delay_accuracy}</td>
      </tr>
    );
  }
}


export default AlertEvent;
