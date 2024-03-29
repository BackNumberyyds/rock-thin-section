import React, { Component } from "react";
import ReactApexChart from "react-apexcharts";
import { VictoryChart, VictoryScatter, VictoryTheme, VictoryAxis, VictoryLabel } from "victory";

const options = {
    chart: {
        type: "scatter",
        zoom: {
            enabled: true,
            type: "xy"
        }
    },
    xaxis: {
        type: "numeric"
    },
    yaxis: {
        type: "category",
        categories: ["Category 1", "Category 2", "Category 3"]
    },
    tooltip: {
        custom: function ({ series, seriesIndex, dataPointIndex, w }) {
            return (
                "<div class='tooltip'>" +
                "<span>Category: " +
                w.config.yaxis[0].categories[series[seriesIndex][dataPointIndex].y] +
                "</span><br>" +
                "<span>X value: " +
                series[seriesIndex][dataPointIndex].x +
                "</span><br>" +
                "<span>Y value: " +
                series[seriesIndex][dataPointIndex].y +
                "</span>" +
                "</div>"
            );
        }
    },
    series: [
        {
            name: "Series 1",
            data: [
                { x: 10, y: 0 },
                { x: 20, y: 1 },
                { x: 30, y: 2 },
                { x: 40, y: 1 },
                { x: 50, y: 0 }
            ]
        }
    ]
}

export class LayerChart extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            series: props.data,
            options: {
                chart: {
                    height: 350,
                    type: 'rangeBar',
                    toolbar: {
                        show: false
                    },
                    zoom: {
                        enabled: false
                    }
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

export class SampleNameChart extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            data: props.data.data,
            categories: props.data.categories
        }
    }

    render() {
        return (
            <VictoryChart height={250}>
                <VictoryAxis
                    tickValues={this.state.categories}
                    tickLabelComponent={
                        <VictoryLabel angle={315} style={{ fontSize: 8 }} />
                    }
                    style={{
                        grid: { stroke: "grey" },
                        ticks: { stroke: "grey", size: 5 },
                    }}
                />

                <VictoryAxis
                    dependentAxis
                    label="井深"
                    style={{
                        axisLabel: { fontSize: 12 },
                        ticks: { stroke: "grey", size: 5 },
                        tickLabels: { fontSize: 8, padding: 3 }
                    }}
                />
                <VictoryScatter
                    style={{ data: { fill: "#c43a31" } }}
                    size={3}
                    data={this.state.data}
                />
            </VictoryChart>
        )
    }
}

function generateRandomCompositions(xrange, yrange) {
    var x = xrange[0];
    var series = [], step, yvalue;
    while (x < xrange[1]) {
        yvalue = Math.round(Math.random() * 3);
        step = Math.round(Math.random() * 10) + 1
        for (let i = 0; i < step * 6; i += 6) {
            series.push([x + i, yvalue]);
        }
        x += step * 6;
    }
    return series;
}


export class RockCompositionChart extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            series: props.data,
            // series: [
            //     {
            //         name: '粗砂岩',
            //         data: generateRandomCompositions([2500, 2900], [0, 3])
            //     },
            //     {
            //         name: '粉砂岩',
            //         data: generateRandomCompositions([2500, 2900], [0, 3])
            //     },
            //     {
            //         name: '玄武岩',
            //         data: generateRandomCompositions([2500, 2900], [0, 3])
            //     },
            //     {
            //         name: '细粒砂岩',
            //         data: generateRandomCompositions([2500, 2900], [0, 3])
            //     },
            //     {
            //         name: '花岗斑岩',
            //         data: generateRandomCompositions([2500, 2900], [0, 3])
            //     },
            //     {
            //         name: '火山角砾岩',
            //         data: generateRandomCompositions([2500, 2900], [0, 3])
            //     },
            //     {
            //         name: '流纹岩',
            //         data: generateRandomCompositions([2500, 2900], [0, 3])
            //     }
            // ],
            options: {
                chart: {
                    type: 'area',
                    height: 350,
                    stacked: true
                },
                colors: [
                    "#008FFB", "#00E396", "#FEB019", "#FF4560", "#775DD0",
                    "#3F51B5", "#546E7A", "#D4526E", "#8D5B4C", "#F86624",
                    "#D7263D", "#1B998B", "#2E294E", "#F46036", "#E2C044"
                ],
                dataLabels: {
                    enabled: false
                },
                stroke: {
                    curve: 'smooth'
                },
                fill: {
                    type: 'gradient',
                    gradient: {
                        opacityFrom: 0.6,
                        opacityTo: 0.8,
                    }
                },
                legend: {
                    position: 'right',
                    horizontalAlign: 'left'
                },
                xaxis: {
                    type: 'numeric'
                },
            },
        };
    }

    render() {
        return (
            <div id="chart">
                <ReactApexChart options={this.state.options} series={this.state.series} type="area" height={350} />
            </div>
        );
    }
}