import React from 'react';
import { connect } from 'react-redux';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, Text } from 'recharts';
import Moment from 'moment';

const VerticalTick = (props) => {
  const { x, y, payload } = props;
  return (
    <g transform={`translate(${x},${y})`} width={70}>
      <Text x={0} y={0} dy={16} textAnchor="end" fill="#666" angle={-35}>
        {payload.value}
      </Text>
    </g>
  );
};

class AccuracyChart extends React.Component {
  render() {
    const dateFmt = 'MM/DD/YY';
    const { alertEvents } = this.props;
    const data = [];
    const dates = alertEvents.map(ae => ae.date);
    const minDate = Moment.min([Moment(), ...dates]);
    const maxDate = Moment.max([minDate, ...dates]);
    const counts = {};
    alertEvents.forEach((item) => {
      const date = item.date.format(dateFmt);
      if (item.delay_accuracy === 'accurate') {
        counts[date] = (counts[date] || 0) + 1;
      }
    });
    const today = Moment();
    if (Object.keys(counts).length > 0) {
      for (let d = Moment(minDate); d <= maxDate && d <= today; d = d.add(1, 'days')) {
        const dateString = d.format(dateFmt);
        const point = { date: dateString };
        if (counts[dateString] != null) {
          point.ontime = counts[dateString] || 0;
        }
        data.push(point);
      }
    }
    const tickInterval = Math.round(maxDate.diff(minDate, 'days') / 6.0) - 1;
    return (
      <fieldset>
        <legend>Accuracy</legend>
        <LineChart width={300} height={350} data={data} margin={{ top: 30, right: 5, bottom: 5, left: 0 }} style={{ lineHeight: '15px' }}>
          <Line name="Trains matching predicted delay" type="monotone" dataKey={'ontime'} stroke="#3a3" activeDot={{ r: 8 }} />
          <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
          <XAxis dataKey={'date'} type="category" tick={<VerticalTick />} interval={tickInterval} />
          <YAxis dataKey={'ontime'} />
          <Tooltip />
          <Legend align="left" wrapperStyle={{ marginLeft: 60, paddingTop: 40 }} />
        </LineChart>
      </fieldset>
    );
  }
}

export default connect(data => ({ alertEvents: data.trainFilteredData }))(AccuracyChart);
