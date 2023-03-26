import React, { Component } from "react";
import ReactApexChart from "react-apexcharts";

const data = [
    {
        name: '中生界',
        data: [
            {
                x: '界',
                y: [
                    0,
                    676.1
                ]
            }
        ]
    },
    {
        name: '上古生界',
        data: [
            {
                x: '界',
                y: [
                    676.1,
                    766
                ]
            }
        ]
    },
    {
        name: '白垩系',
        data: [
            {
                x: '系',
                y: [
                    0,
                    538
                ]
            }
        ]
    },
    {
        name: '侏罗系',
        data: [
            {
                x: '系',
                y: [
                    538,
                    676.1
                ]
            }
        ]

    },
    {
        name: '石炭系',
        data: [
            {
                x: '系',
                y: [
                    676.1,
                    766
                ]
            }
        ]

    },
    {
        name: '中统',
        data: [
            {
                x: '统',
                y: [
                    538,
                    594.7
                ]
            }
        ]
    },
    {
        name: '下统',
        data: [
            {
                x: '统',
                y: [
                    594.7,
                    676.1
                ]
            }
        ]
    },
    {
        name: '西山窑组',
        data: [
            {
                x: '组',
                y: [
                    538,
                    594.7
                ]
            }
        ]
    },
    {
        name: '三工河组',
        data: [
            {
                x: '组',
                y: [
                    594.7,
                    605
                ]
            }
        ]
    },
    {
        name: '八道湾组',
        data: [
            {
                x: '组',
                y: [
                    605,
                    676.1
                ]
            }
        ]
    }
]

class LayerChart extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            isLoading: true,
            series: data,
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

    // async componentDidMount() {
    //     // 设置状态为正在加载
    //     this.setState({ isLoading: true });
    //     try {
    //         const response = await fetch("/api/allphotoform-datas/");
    //         const data = await response.json();

    //         // 数据回显
    //         if (data.hasOwnProperty("form_data")) {
    //             const isAllDepth = data.form_data.hasOwnProperty("is_all_depth");
    //             const isRangeSearch = data.form_data.hasOwnProperty("is_range_search");
    //             if (!isAllDepth) {
    //                 this.setState({ lowDepth: data.form_data.depth_low })
    //                 if (isRangeSearch) {
    //                     this.setState({ highDepth: data.form_data.depth_high })
    //                 }
    //             }
    //             this.setState({
    //                 minesChecked: data.form_data.mines_selected.split(",").map(e => e + "-mine"),
    //                 lensChecked: data.form_data.lens_selected.split(","),
    //                 orthsChecked: data.form_data.orths_selected.split(","),
    //                 isAllDepth: isAllDepth,
    //                 isRangeSearch: isRangeSearch,
    //             })
    //         }
    //         console.log(data);

    //         this.setState({
    //             nodesData: data,
    //             isLoading: false,
    //             minesExpanded: getNodeIds(data.regions),
    //             lensExpanded: getNodeIds(data.lens),
    //             orthsExpanded: getNodeIds(data.orths)
    //         });
    //     } catch (error) {
    //         console.error(error);
    //     }
    // }

    render() {
        return (
            <div id="chart">
                <ReactApexChart options={this.state.options} series={this.state.series} type="rangeBar" height={350} />
            </div>
        );
    }
}

export default LayerChart;