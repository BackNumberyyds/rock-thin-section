import React from 'react';
import CheckboxTree from 'react-checkbox-tree';
import 'react-checkbox-tree/lib/react-checkbox-tree.css';
import Collapse from './collapse';

const nodes = [{
    value: 'diqu',
    label: '地区',
    children: [
        {
            value: 'zhunxi',
            label: '准西'
        },
        {
            value: 'zhunxibei',
            label: '准西北',
            children: [
                {
                    value: 'haqian217',
                    label: '哈浅217井'
                },
                {
                    value: 'haqian218',
                    label: '哈浅218井'
                },
            ],
        },
    ],
}];

const data = {
    regions: [{
        value: 'diqu',
        label: '地区',
        children: [
            {
                value: 'zhunxi',
                label: '准西'
            },
            {
                value: 'zhunxibei',
                label: '准西北',
                children: [
                    {
                        value: 'haqian217',
                        label: '哈浅217井'
                    },
                    {
                        value: 'haqian218',
                        label: '哈浅218井'
                    },
                ],
            },
        ],
    }],
    lens: [{
        value: 'wujingbeishu',
        label: '物镜倍数',
        children: [
            {
                value: 4,
                label: '4X'
            },
            {
                value: 10,
                label: '10X'
            }]
    }],
    orths: [{
        value: 'zhengjiaopianguang',
        label: '正交偏光',
        children: [
            {
                value: 'o',
                label: '正交'
            },
            {
                value: 'p',
                label: '单偏'
            }
        ]
    }]
}

class DepthInputField extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            collapsed: true
        }
        this.handleCollapse = this.handleCollapse.bind(this);
    }

    handleCollapse() {
        this.setState(function (state, props) {
            return {
                collapsed: !state.collapsed
            };
        });
    }

    render() {
        return (
            <Collapse header="井深">
                <ul className="btn-toggle-nav list-unstyled pb-1">
                    <div className="row g-3 pt-2">
                        <div className="col-6 ps-4">
                            <div className="form-check form-switch">
                                <input className="form-check-input" type="checkbox" role="switch" id="is_all_depth" name="is_all_depth" />
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
            // <div className="react-checkbox-tree rct-icons-fa4">
            //     <div>
            //         <Collapse header="Click to toggle">
            //             <p>Some content here...</p>
            //         </Collapse>
            //     </div>
            //     <ol>
            //         <li className="rct-node rct-node-parent rct-node-expanded">
            //             <span className="rct-text">
            //                 <button
            //                     data-bs-toggle="collapse"
            //                     href="#collapseExample"
            //                     type="button"
            //                     className="rct-collapse rct-collapse-btn"
            //                     onClick={this.handleCollapse}
            //                 >
            //                     <span className={"rct-icon " + (this.state.collapsed ? "rct-icon-expand-close" : "rct-icon-expand-open")}></span>
            //                 </button>
            //                 <label for="rct-V5GdGs-iIg5AE27tlhlWf-diqu">
            //                     <input id="rct-V5GdGs-iIg5AE27tlhlWf-diqu" type="checkbox" />
            //                     <span aria-checked="false" aria-disabled="false" className="rct-checkbox" role="checkbox" tabindex="0">
            //                         <span className="rct-icon rct-icon-uncheck"></span>
            //                     </span>
            //                     <span className="rct-node-icon" />
            //                     <span className="rct-title">地区</span>
            //                 </label>
            //             </span>
            //             <div id="collapseExample" className="collapse">123</div>
            //         </li>
            //     </ol >
            // </div >
        );
    }
}

class SearchForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            mines_checked: [],
            lens_checked: [],
            orths_checked: [],
            mines_expanded: data.regions.map(n => n.value),
            lens_expanded: data.lens.map(n => n.value),
            orths_expanded: data.orths.map(n => n.value)
        };
        this.submitform = this.submitform.bind(this);
    }

    submitform() {
        console.log('submit');
    }

    render() {
        console.log(this.state.mines_checked);
        console.log(this.state.lens_checked);
        return (
            <form method="post" action="">
                <input type="hidden" name="csrfmiddlewaretoken" value={window.csrf_token} />
                <CheckboxTree
                    nodes={data.regions}
                    checked={this.state.mines_checked}
                    expanded={this.state.mines_expanded}
                    onCheck={checked => this.setState({ mines_checked: checked })}
                    onExpand={mines_expanded => this.setState({ mines_expanded })}
                />
                <DepthInputField />
                <CheckboxTree
                    nodes={data.lens}
                    checked={this.state.lens_checked}
                    expanded={this.state.lens_expanded}
                    onCheck={checked => this.setState({ lens_checked: checked })}
                    onExpand={lens_expanded => this.setState({ lens_expanded })}
                />
                <CheckboxTree
                    nodes={data.orths}
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

class MyForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            checked: [],
        };
    }

    handleSubmit = (event) => {
        event.preventDefault();
        console.log('Checked items:', this.state.checked);
        // 在这里处理表单提交逻辑
    };

    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                <label>My Checkbox Tree</label>
                <CheckboxTree
                    nodes={nodes}
                    checked={this.state.checked}
                    expanded={this.state.expanded}
                    onCheck={checked => this.setState({ checked })}
                    onExpand={expanded => this.setState({ expanded })}
                />
                <button type="submit">Submit</button>
            </form>
        );
    }
}

export default SearchForm;