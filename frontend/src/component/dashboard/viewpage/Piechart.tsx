import React, { useEffect, useState } from 'react';
import { PieChart } from '@mui/x-charts/PieChart';
import axios from "axios"

export default function Prechart({ segment_id, labelMap }) {

    const [pieData, setPieData] = useState([])
    useEffect(() => {
        axios({
            url: "/api/getLabelArea/",
            method: "GET",
            headers: {},
            params: {
                segment_image_id: segment_id,
            }
        }).then((res) => {
            console.log("/api/getLabelArea/:", res)
            let tempPieChart = labelMap.map(item => {
                return { id: item.id, label: item.name, color: item.color, value: res.data.segment_area[`${item.id}`] ? res.data.segment_area[`${item.id}`] : 0 }
            })
            console.log("tempPieChart:", tempPieChart)
            setPieData(tempPieChart)
        }).catch((err) => { console.log(err) });
    }, [])
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