import React from 'react';
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

export default () => {
  const data = [
      { time: '60+ early', rate: 5 },
      { time: '40-60 early', rate: 10 },
      { time: '20-40 early', rate: 15 },
      { time: '0-20 early', rate: 20 },
      { time: '0-20 late', rate: 20 },
      { time: '20-40 late', rate: 15 },
      { time: '40-60 late', rate: 10 },
      { time: '60+ late', rate: 5 },
  ];

  return (
    <fieldset>
      <legend>Timeliness</legend>
      <BarChart width={300} height={350} data={data} margin={{ top: 30, right: 5, bottom: 62 }} >
        <Bar name="rate" dataKey="rate" fill="#3c3" label unit="%" />
        <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
        <XAxis dataKey="time" tickLine={false} tick={<VerticalTick />} interval={0} />
        <YAxis dataKey="rate" label="%" />
        <Tooltip />
      </BarChart>
    </fieldset>
  );
};
