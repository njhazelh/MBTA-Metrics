import React from 'react';
import { Button } from 'reactstrap';
import { connect } from 'react-redux';

class CSVDownloadButton extends React.Component {
  downloadCSV() {
    let { alertEvents } = this.props;
    const timeFmt = 'H:mm A';

    if (alertEvents.length === 0) {
      console.info('No alertEvents to download');
      return;
    }
    console.info('Download started');


    alertEvents = alertEvents.map(item => ({
      ...item,
      date: item.date && item.date.format('YYYY-MM-DD'),
      time: item.time && item.time.format(timeFmt),
      scheduled_departure: item.scheduled_departure && item.scheduled_departure.format(timeFmt),
      actual_departure: item.actual_departure && item.actual_departure.format(timeFmt),
    }));

    const escapeField = (item) => {
      if (typeof (item) === 'string') {
        return `"${item.replace('"', '""')}"`;
      }
      return item;
    };

    const keys = Object.keys(alertEvents[0]);
    let csv = `${keys.map(escapeField).join(',')}\n`;

    alertEvents.forEach((item) => {
      const values = keys.map(key => escapeField(item[key]));
      csv += `${values.join(',')}\n`;
    });

    const link = document.createElement('a');
    link.href = `data:text/csv;charset=utf-8,${encodeURI(csv)}`;
    link.target = '_blank';
    link.download = 'alert_metrics.csv';
    link.click();
  }

  render() {
    return (
      <Button onClick={() => this.downloadCSV()} color="primary" style={{ float: 'right' }}>
        Download as CSV
      </Button>
    );
  }
}

export default connect(data => ({ alertEvents: data.alertFilteredData }))(CSVDownloadButton);
