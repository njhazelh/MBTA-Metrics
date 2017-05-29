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

class ExistenceChart extends React.Component {
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
      if (counts[date] == null) {
        counts[date] = {};
      }
      if (item.alert_issued && item.deserves_alert) {
        counts[date].delayed = (counts[date].delayed || 0) + 1;
      } else if (item.alert_issued && !item.deserves_alert) {
        counts[date].undelayed = (counts[date].undelayed || 0) + 1;
      }
    });
    const today = Moment();
    if (Object.keys(counts).length > 0) {
      for (let d = Moment(minDate); d <= maxDate && d <= today; d = d.add(1, 'days')) {
        const dateString = d.format(dateFmt);
        const point = { date: dateString };
        if (counts[dateString] != null) {
          point.delayed = counts[dateString].delayed;
          point.non_delayed = counts[dateString].undelayed;
        }
        data.push(point);
      }
    }
    const tickInterval = Math.round(maxDate.diff(minDate, 'days') / 6.0) - 1;
    return (
      <fieldset>
        <legend>Existence</legend>
        <LineChart width={300} height={350} data={data} margin={{ top: 30, right: 5, bottom: 25, left: 0 }} style={{ lineHeight: '15px' }}>
          <Line name="Delayed Trains had alerts" type="monotone" dataKey={'delayed'} stroke="#3a3" activeDot={{ r: 8 }} />
          <Line name="Non-delayed Trains had alerts" type="monotone" dataKey={'non_delayed'} stroke="#a33" activeDot={{ r: 8 }} />
          <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
          <XAxis dataKey="date" type="category" interval={tickInterval} tick={<VerticalTick />} />
          <YAxis name="Existence" />
          <Tooltip />
          <Legend
            align="left"
            wrapperStyle={{
              marginLeft: 60,
              paddingTop: 40,
              width: 265,
              height: 30,
            }}
          />
        </LineChart>
      </fieldset>
    );
  }
}

export default connect(data => ({ alertEvents: data.trainFilteredData }))(ExistenceChart);
