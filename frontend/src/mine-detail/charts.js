import React, { Component } from "react";
import ReactApexChart from "react-apexcharts";

export class LayerChart extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            series: props.data,
            options: {
                chart: {
                    height: 350,
                    type: 'rangeBar'
                },
                plotOptions: {
                    bar: {
                        horizontal: true,
                        barHeight: '50%',
                        rangeBarGroupRows: true
                    }
                },
                colors: [
                    "#008FFB", "#00E396", "#FEB019", "#FF4560", "#775DD0",
                    "#3F51B5", "#546E7A", "#D4526E", "#8D5B4C", "#F86624",
                    "#D7263D", "#1B998B", "#2E294E", "#F46036", "#E2C044"
                ],
                fill: {
                    type: 'solid'
                },
                xaxis: {
                    type: 'numeric'
                },
                legend: {
                    position: 'right'
                },
                tooltip: {
                    y: {
                        formatter: function (value, seriesIndex) {
                            return Number(value).toFixed(2).replace(/\.?0+$/, '') + 'm';
                        }
                    }
                }
            },
        };
    }

    render() {
        return (
            <div id="chart">
                <ReactApexChart options={this.state.options} series={this.state.series} type="rangeBar" height={350} />
            </div>
        );
    }
}

// 定义数据和选项
const data = [
    {
        name: 'Sample A',
        data: [[10, 5], [20, 10], [30, 15], [40, 20]]
    },
    {
        name: 'Sample B',
        data: [[10, 15], [20, 20], [30, 25], [40, 30]]
    }
]

var options = {
    chart: {
        type: 'scatter'
    },
    series: [
        {
            name: 'Sales',
            data: [
                { x: 'North', y: 30 },
                { x: 'South', y: 40 },
                { x: 'East', y: 35 },
                { x: 'West', y: 50 },
                { x: 'Central', y: 49 }
            ]
        },
        {
            name: 'Sales',
            data: [
                { x: 'North', y: 30 },
                { x: 'South', y: 40 },
                { x: 'East', y: 35 },
                { x: 'West', y: 50 },
                { x: 'Central', y: 49 }
            ]
        }
    ],
    xaxis: {
        type: 'category',
        categories: ['North', 'South', 'East', 'West', 'Central']
    }
}

export class SampleNameChart extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return <ReactApexChart options={options} series={options.series} type="scatter" height={350} />
    }
}