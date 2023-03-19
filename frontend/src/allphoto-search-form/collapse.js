import React, { Component } from 'react';

class Collapse extends Component {
    constructor(props) {
        super(props);
        this.state = {
            collapsed: props.collapsed || false
        };
    }

    toggleCollapse = () => {
        this.setState(function (state, props) {
            return {
                collapsed: !state.collapsed
            };
        });
    }

    render() {
        const { header, children } = this.props;
        const { collapsed } = this.state;

        return (
            <div className="react-checkbox-tree rct-icons-fa4 rct-native-display">
                <ol>
                    <li className="rct-node rct-node-parent rct-node-expanded">
                        <span className="rct-text">
                            <button
                                type="button"
                                className="rct-collapse rct-collapse-btn"
                                onClick={this.toggleCollapse}
                            >
                                <span className={"rct-icon " + (this.state.collapsed ? "rct-icon-expand-close" : "rct-icon-expand-open")}></span>
                            </button>
                            <label>
                                <span aria-checked="false" className="native-checkbox" aria-disabled="false" role="checkbox" tabindex="0">
                                    <span className="rct-icon rct-icon-uncheck"></span>
                                </span>
                                <span className="rct-node-icon" />
                                <span className="rct-title">{this.props.header}</span>
                            </label>
                        </span>
                        {!this.state.collapsed && <div>{children}</div>}
                    </li>
                </ol >
            </div >
        );
    }
}

export default Collapse;
