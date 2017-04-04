import React from 'react';
import {LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, Text} from 'recharts';

const VerticalTick = (props) => {
  const {x, y, stroke, payload} = props;
  return (
    <g transform={`translate(${x},${y})`} width={70}>
      <Text x={0} y={0} dy={16} textAnchor="end" fill="#666" angle={-35}>
        {payload.value}
      </Text>
    </g>
  );
}

export default () => {
  let data=[
    {date: new Date(2017, 1, 1), ontime: 50},
    {date: new Date(2017, 1, 2), ontime: 60},
    {date: new Date(2017, 1, 3), ontime: 70},
    {date: new Date(2017, 1, 4), ontime: 66},
    {date: new Date(2017, 1, 5), ontime: 73},
    {date: new Date(2017, 1, 6), ontime: 80},
    {date: new Date(2017, 1, 7), ontime: 81},
    {date: new Date(2017, 1, 8), ontime: 80},
    {date: new Date(2017, 1, 9)},
    {date: new Date(2017, 1, 10), ontime: 80}
  ];
  data = data.map(point => {
    point.date = point.date.toLocaleDateString()
    return point;
  })
  return (
    <fieldset>
      <legend>Accuracy</legend>
      <LineChart width={300} height={350} data={data} margin={{top:30, right: 5, bottom: 5, left: 0}} style={{lineHeight:'15px'}}>
        <Line name="Trains matching predicted delay" type="monotone" dataKey={"ontime"} stroke="#3a3" activeDot={{r: 8}} unit="%"/>
        <CartesianGrid stroke="#ccc" strokeDasharray="5 5"/>
        <XAxis dataKey={"date"} type="category" tick={<VerticalTick/>} interval={0}/>
        <YAxis dataKey={"ontime"}/>
        <Tooltip />
        <Legend align='left' wrapperStyle={{marginLeft: 60, paddingTop: 40}}/>
      </LineChart>
    </fieldset>
  );
}
