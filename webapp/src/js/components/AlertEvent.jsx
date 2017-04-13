import React from 'react';

const TIME_FORMAT = 'h:mm A';
const DATE_FORMAT = 'MM/DD/YYYY';

class AlertEvent extends React.Component {
  render() {
    const { data } = this.props;
    return (
      <tr>
        <td>{data.trip_id}</td>
        <td>
          {
            data.date != null
            ? data.date.format(DATE_FORMAT)
            : ''
          }
        </td>
        <td>
          {
            data.time != null
            ? data.time.format(TIME_FORMAT)
            : ''
          }
        </td>
        <td>
          {
            data.date != null
            ? data.date.format('dddd')
            : ''
          }
        </td>
        <td>{data.route}</td>
        <td>{data.stop}</td>
        <td>{data.direction}</td>
        <td>{data.short_name}</td>
        <td>
          {
            data.scheduled_departure != null
            ? data.scheduled_departure.format(TIME_FORMAT)
            : ''
          }
        </td>
        <td>
          {
            data.actual_departure != null
            ? data.actual_departure.format(TIME_FORMAT)
            : ''
          }
        </td>
        <td>
          {
            data.actual_departure != null && data.scheduled_departure != null
            ? `${data.actual_departure.diff(data.scheduled_departure, 'minutes')} min`
            : ''
          }
        </td>
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
