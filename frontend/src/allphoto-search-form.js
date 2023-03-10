import React, { useState, useEffect } from 'react';
import CheckboxTree from 'react-checkbox-tree';
import 'react-checkbox-tree/lib/react-checkbox-tree.css';
import Collapse from './collapse';

class DepthInputField extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            collapsed: true,
            isAllDepth: false,
            isRangeSearch: false
        }
    }

    toggleAllDepth = () => {
        this.setState(() => { isAllDepth: !this.state.isAllDepth });
    }

    render() {
        return (
            <Collapse header="井深">
                <ul className="btn-toggle-nav list-unstyled pb-1">
                    <div className="row g-3 pt-2">
                        <div className="col-6 ps-4">
                            <div className="form-check form-switch">
                                <input className="form-check-input" type="checkbox" role="switch" id="is_all_depth" name="is_all_depth" onChange={this.toggleAllDepth} />
                                <label className="form-check-label btn-toggle-2" for="is_all_depth">全部井深</label>
                            </div>
                        </div>
                        <div className="col-6 ps-3">
                            <div className="form-check form-switch">
                                <input className="form-check-input" type="checkbox" role="switch" id="is_range_search" name="is_range_search" />
                                <label className="form-check-label btn-toggle-2" for="is_range_search">范围筛选</label>
                            </div>
                        </div>
                    </div>
                    <div className="row g-3 pt-2 mb-2">
                        <div className="col-5 ps-3 pe-0">
                            <div className="input-group input-group-sm">
                                <input type="number" name="depth_low" className="form-control" min="0" max="1000" required="" step="any" id="id_depth_low" />
                                <span className="input-group-text">m</span>
                            </div>
                        </div>
                        <div className="col-2 text-center px-0" style={{ fontWeight: 500, color: "grey" }}>—</div>
                        <div className="col-5 pe-3 ps-0">
                            <div className="input-group input-group-sm">
                                <input type="number" name="depth_high" className="form-control" min="0" max="1000" required="" disabled="" step="any" id="id_depth_high" />
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
            mines_checked: [],
            lens_checked: [],
            orths_checked: [],
            mines_expanded: [],
            lens_expanded: [],
            orths_expanded: [],
            nodesData: null,
            isLoading: true,
            error: null,
        };
        this.submitform = this.submitform.bind(this);
    }

    async componentDidMount() {
        // 设置状态为正在加载
        this.setState({ isLoading: true });
        try {
            const response = await fetch("/api/allphotoform-datas/");
            const data = await response.json();

            this.setState({
                nodesData: data,
                isLoading: false,
                mines_expanded: getNodeIds(data.regions),
                lens_expanded: getNodeIds(data.lens),
                orths_expanded: getNodeIds(data.orths)
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
                    <CheckboxTree
                        nodes={this.state.nodesData.regions}
                        checked={this.state.mines_checked}
                        expanded={this.state.mines_expanded}
                        onCheck={checked => this.setState({ mines_checked: checked })}
                        onExpand={mines_expanded => this.setState({ mines_expanded })}
                    />
                    <DepthInputField />
                    <CheckboxTree
                        nodes={this.state.nodesData.lens}
                        checked={this.state.lens_checked}
                        expanded={this.state.lens_expanded}
                        onCheck={checked => this.setState({ lens_checked: checked })}
                        onExpand={lens_expanded => this.setState({ lens_expanded })}
                    />
                    <CheckboxTree
                        nodes={this.state.nodesData.orths}
                        checked={this.state.orths_checked}
                        expanded={this.state.orths_expanded}
                        onCheck={checked => this.setState({ orths_checked: checked })}
                        onExpand={orths_expanded => this.setState({ orths_expanded })}
                    />
                    <div className="d-grid gap-2">
                        <button className="btn btn-primary" onClick={this.submitform} type="button">筛选</button>
                    </div>
                </form>
            );
        }
    }
}

export default SearchForm;