import React, { useState, useEffect } from 'react';
import CheckboxTree from 'react-checkbox-tree';
import 'react-checkbox-tree/lib/react-checkbox-tree.css';
import Collapse from './collapse';

class DepthInputField extends React.Component {
    constructor(props) {
        super(props);
    }

    handleChange = (e, a) => {
        this.props.onDepthInputChange(e.target.value, a);
    }

    render() {
        return (
            <Collapse header="井深">
                <ul className="btn-toggle-nav list-unstyled pb-1">
                    <div className="row g-3 pt-2">
                        <div className="col-6 ps-4">
                            <div className="form-check form-switch">
                                <input className="form-check-input" type="checkbox" role="switch" id="is_all_depth" name="is_all_depth"
                                    checked={this.props.isAllDepth}
                                    onChange={this.props.onAllDepthChange} />
                                <label className="form-check-label btn-toggle-2" for="is_all_depth">全部井深</label>
                            </div>
                        </div>
                        <div className="col-6 ps-3">
                            <div className="form-check form-switch">
                                <input className="form-check-input" type="checkbox" role="switch" id="is_range_search" name="is_range_search"
                                    checked={this.props.isRangeSearch}
                                    onChange={this.props.onRangeSearchChange}
                                    disabled={this.props.isAllDepth} />
                                <label className="form-check-label btn-toggle-2" for="is_range_search">范围筛选</label>
                            </div>
                        </div>
                    </div>
                    <div className="row g-3 pt-2 mb-2">
                        <div className="col-5 ps-3 pe-0">
                            <div className="input-group input-group-sm">
                                <input type="number" name="depth_low" className="form-control" min="0" max="1000" required="" step="any" id="id_depth_low"
                                    value={this.props.lowDepth}
                                    onChange={(event) => this.handleChange(event, 0)}
                                    disabled={this.props.isAllDepth} />
                                <span className="input-group-text">m</span>
                            </div>
                        </div>
                        <div className="col-2 text-center px-0" style={{ fontWeight: 500, color: "grey" }}>—</div>
                        <div className="col-5 pe-3 ps-0">
                            <div className="input-group input-group-sm">
                                <input type="number" name="depth_high" className="form-control" min="0" max="1000" required="" step="any" id="id_depth_high"
                                    value={this.props.highDepth}
                                    onChange={(event) => this.handleChange(event, 1)}
                                    disabled={this.props.isAllDepth || !this.props.isRangeSearch} />
                                <span className="input-group-text">m</span>
                            </div>
                        </div>
                    </div>
                </ul>
            </Collapse>
        );
    }
}

const getNodeIds = (nodes) => {
    let ids = [];

    nodes?.forEach(({ value, children }) => {
        ids = [...ids, value, ...getNodeIds(children)];
    });

    return ids;
};

class SearchForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            minesChecked: [],
            lensChecked: [],
            orthsChecked: [],
            minesExpanded: [],
            lensExpanded: [],
            orthsExpanded: [],
            lowDepth: "",
            highDepth: "",
            nodesData: null,
            isLoading: true,
            isAllDepth: false,
            isRangeSearch: false,
        };
        this.submitform = this.submitform.bind(this);
    }

    toggleAllDepth = () => {
        if (!this.state.isAllDepth) {
            this.setState({
                lowDepth: "",
                highDepth: "",
                isRangeSearch: false
            })
        }
        this.setState({ isAllDepth: !this.state.isAllDepth });
    }

    toggleRangeSearch = () => {
        this.setState({ isRangeSearch: !this.state.isRangeSearch });
    }

    onDepthInputChange = (value, a) => {
        if (a == 0) {
            this.setState({ lowDepth: value })
        } else if (a == 1) {
            this.setState({ highDepth: value })
        }
    }

    // 通过api获得表单复选框数据
    async componentDidMount() {
        // 设置状态为正在加载
        this.setState({ isLoading: true });
        try {
            const response = await fetch("/api/allphotoform-datas/");
            const data = await response.json();

            // 数据回显
            if (data.hasOwnProperty("form_data")) {
                const isAllDepth = data.form_data.hasOwnProperty("is_all_depth");
                const isRangeSearch = data.form_data.hasOwnProperty("is_range_search");
                if (!isAllDepth) {
                    this.setState({ lowDepth: data.form_data.depth_low })
                    if (isRangeSearch) {
                        this.setState({ highDepth: data.form_data.depth_high })
                    }
                }
                this.setState({
                    minesChecked: data.form_data.mines_selected.split(",").map(e => e + "-mine"),
                    lensChecked: data.form_data.lens_selected.split(","),
                    orthsChecked: data.form_data.orths_selected.split(","),
                    isAllDepth: isAllDepth,
                    isRangeSearch: isRangeSearch,
                })
            }
            console.log(data);

            this.setState({
                nodesData: data,
                isLoading: false,
                minesExpanded: getNodeIds(data.regions),
                lensExpanded: getNodeIds(data.lens),
                orthsExpanded: getNodeIds(data.orths)
            });
        } catch (error) {
            console.error(error);
        }
    }

    submitform() {
        console.log('submit');
    }

    render() {
        if (!this.state.isLoading) {
            return (
                <form method="post" action="">
                    <input type="hidden" name="csrfmiddlewaretoken" value={window.csrf_token} />
                    <input type="text" name="mines_selected" hidden value={this.state.minesChecked.map(str => str.split("-")[0])} id="id_mines_selected" required />
                    <CheckboxTree
                        nodes={this.state.nodesData.regions}
                        checked={this.state.minesChecked}
                        expanded={this.state.minesExpanded}
                        onCheck={checked => this.setState({ minesChecked: checked })}
                        onExpand={minesExpanded => this.setState({ minesExpanded })}
                    />
                    <DepthInputField
                        isAllDepth={this.state.isAllDepth}
                        isRangeSearch={this.state.isRangeSearch}
                        lowDepth={this.state.lowDepth}
                        highDepth={this.state.highDepth}
                        onDepthInputChange={this.onDepthInputChange}
                        onAllDepthChange={this.toggleAllDepth}
                        onRangeSearchChange={this.toggleRangeSearch}
                    />
                    <input type="text" name="lens_selected" hidden value={this.state.lensChecked} id="id_lens_selected" required />
                    <CheckboxTree
                        nodes={this.state.nodesData.lens}
                        checked={this.state.lensChecked}
                        expanded={this.state.lensExpanded}
                        onCheck={checked => this.setState({ lensChecked: checked })}
                        onExpand={lensExpanded => this.setState({ lensExpanded })}
                    />
                    <input type="text" name="orths_selected" hidden value={this.state.orthsChecked} id="id_orths_selected" required />
                    <CheckboxTree
                        nodes={this.state.nodesData.orths}
                        checked={this.state.orthsChecked}
                        expanded={this.state.orthsExpanded}
                        onCheck={checked => this.setState({ orthsChecked: checked })}
                        onExpand={orthsExpanded => this.setState({ orthsExpanded })}
                    />
                    <div className="d-grid gap-2">
                        <button className="btn btn-primary" type="submit">筛选</button>
                        {/* <button className="btn btn-primary" onClick={this.submitform} type="button">筛选</button> */}
                    </div>
                </form>
            );
        }
    }
}

export default SearchForm;