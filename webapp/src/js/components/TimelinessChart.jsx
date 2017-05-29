import React from 'react';
import { connect } from 'react-redux';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Text } from 'recharts';

const VerticalTick = (props) => {
  const { x, y, payload } = props;
  return (
    <g transform={`translate(${x},${y})`} width={70}>
      <Text x={0} y={0} textAnchor="end" fill="#666" angle={-90}>
        {payload.value}
      </Text>
    </g>
  );
};

class TimelinessChart extends React.Component {
  render() {
    const { alertEvents } = this.props;
    const data = (alertEvents != null && Array.isArray(alertEvents) && alertEvents.length > 0)
      ? [
        { time: '60+ early', rate: alertEvents.filter(ae => ae.alert_delay <= -60).length },
        { time: '40-60 early', rate: alertEvents.filter(ae => ae.alert_delay <= -40 && ae.alert_delay > -60).length },
        { time: '20-40 early', rate: alertEvents.filter(ae => ae.alert_delay <= -20 && ae.alert_delay > -40).length },
        { time: '0-20 early', rate: alertEvents.filter(ae => ae.alert_delay < 0 && ae.alert_delay > -20).length },
        { time: '0-20 late', rate: alertEvents.filter(ae => ae.alert_delay >= 0 && ae.alert_delay < 20).length },
        { time: '20-40 late', rate: alertEvents.filter(ae => ae.alert_delay >= 20 && ae.alert_delay < 40).length },
        { time: '40-60 late', rate: alertEvents.filter(ae => ae.alert_delay >= 40 && ae.alert_delay < 60).length },
        { time: '60+ late', rate: alertEvents.filter(ae => ae.alert_delay >= 60).length },
      ] : [];

    return (
      <fieldset>
        <legend>Timeliness</legend>
        <BarChart width={300} height={350} data={data} margin={{ top: 30, right: 5, bottom: 62 }} >
          <Bar name="rate" dataKey="rate" fill="#3c3" label />
          <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
          <XAxis dataKey="time" tickLine={false} tick={<VerticalTick />} interval={0} />
          <YAxis dataKey="rate" />
          <Tooltip />
        </BarChart>
      </fieldset>
    );
  }
}


export default connect(data => ({ alertEvents: data.trainFilteredData }))(TimelinessChart);
