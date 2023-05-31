import React from "react";
import { AreaChart, ReferenceLine, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

function StockChart(props) {
  const {data, growing} = props;
  
  return (
  <ResponsiveContainer width={500} height={400}>
    <AreaChart data={data} 
     margin={{top: 50, right: 20, bottom: 20, left: 30,}}>
     <XAxis dataKey="date" hide={true}/>
     <YAxis />
     <CartesianGrid strokeDasharray="3 3" />
     <Tooltip />
     <Area type="monotone" dataKey="price" stroke={growing ? "green" : "red" }fill={growing ? "green" : "red" } />
    </AreaChart>
  </ResponsiveContainer>
  )
}

export default StockChart
