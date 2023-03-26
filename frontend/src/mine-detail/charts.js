import React, { Component } from "react";
import ReactApexChart from "react-apexcharts";

class LayerChart extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            isLoading: true,
            series: [],
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
                }
            },
        };
    }

    async componentDidMount() {
        // 设置状态为正在加载
        this.setState({ isLoading: true });
        try {
            const response = await fetch("/api" + window.location.pathname);
            const data = await response.json();
            this.setState({
                series: data,
                isLoading: false
            });
        } catch (error) {
            console.error(error);
        }
    }

    render() {
        return (
            <div id="chart">
                <ReactApexChart options={this.state.options} series={this.state.series} type="rangeBar" height={350} />
            </div>
        );
    }
}

export default LayerChart;