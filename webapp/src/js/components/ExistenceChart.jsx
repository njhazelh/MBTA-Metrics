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
    {date: new Date(2017, 1, 1), delayed: 70, non_delayed: 12},
    {date: new Date(2017, 1, 2), delayed: 85, non_delayed: 19},
    {date: new Date(2017, 1, 3), delayed: 70, non_delayed: 20},
    {date: new Date(2017, 1, 4), delayed: 80, non_delayed: 22},
    {date: new Date(2017, 1, 5), delayed: 80, non_delayed: 22},
    {date: new Date(2017, 1, 6), delayed: 80, non_delayed: 22},
    {date: new Date(2017, 1, 7), delayed: 80, non_delayed: 22},
    {date: new Date(2017, 1, 8), delayed: 80, non_delayed: 22},
    {date: new Date(2017, 1, 9), delayed: 80, non_delayed: 22}
  ];
  data = data.map(point => {
    point.date = point.date.toLocaleDateString()
    return point;
  })
  return (
    <fieldset>
      <legend>Existence</legend>
      <LineChart width={300} height={350} data={data} margin={{top:30, right: 5, bottom: 25, left: 0}} style={{lineHeight:'15px'}}>
        <Line name="Delayed Trains had alerts" type="monotone" dataKey={"delayed"} stroke="#3a3" unit="%" activeDot={{r: 8}}/>
        <Line name="Non-delayed Trains had alerts" type="monotone" dataKey={"non_delayed"} stroke="#a33" unit="%" activeDot={{r: 8}}/>
        <CartesianGrid stroke="#ccc" strokeDasharray="5 5"/>
        <XAxis dataKey="date" type="category" interval={0} tick={<VerticalTick/>}/>
        <YAxis name="Existence" unit="%"/>
        <Tooltip />
        <Legend align='left' wrapperStyle={{marginLeft: 60, paddingTop:40, width:265, height: 30}}/>
      </LineChart>
    </fieldset>
  );
}
