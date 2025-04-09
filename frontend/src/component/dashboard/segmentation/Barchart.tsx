import * as React from 'react';
import { BarChart } from '@mui/x-charts/BarChart';
import { axisClasses } from '@mui/x-charts/ChartsAxis';

export default function Barchart(props) {

    console.log("Barchart props:", props)

    const { data, label, color } = props;

    const chartSetting = {
        yAxis: [
            {
                label: 'Labeled Segments',
            },
        ],
        width: 650,
        height: 200,
        sx: {
            [`.${axisClasses.left} .${axisClasses.label}`]: {
                transform: 'translate(-20px, 0)',
            },
        },
    };

    return (
        <BarChart
            xAxis={[{
                scaleType: 'band', data: label, colorMap: {
                    type: 'ordinal',
                    colors: color
                }
            }]}
            series={[{ data: data }]}
            margin={{ top: 20, bottom: 30, left: 80, right: 10 }}
            {...chartSetting}
        />
    );
}
