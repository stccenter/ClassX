import React, { useEffect, useState } from 'react';
import { PieChart } from '@mui/x-charts/PieChart';

export default function Prechart(props) {
    console.log("Piechart props: ", props)
    const { data, labelClass } = props;
    const [pieData, setPieData] = useState([])
    useEffect(() => {
        let tempData = data
        if (labelClass) {
            labelClass.forEach(item => {
                if (item[0] != 0) {
                    tempData[item[0] - 1].value = item[1];
                }
            })
            console.log("tempData:", tempData)
            setPieData(tempData)
            console.log("pieData:", pieData)
        }
    })
    return (
        <PieChart
            series={[
                {
                    data: pieData,
                },
            ]}
            width={650}
            height={200}
        />
    );
}