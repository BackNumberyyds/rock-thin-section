import React from 'react';
import CheckboxTree from 'react-checkbox-tree';
import 'react-checkbox-tree/lib/react-checkbox-tree.css';

const nodes = [{
    value: 'mars',
    label: '地区',
    children: [
        { value: 'phobos', label: '准西' },
        {
            value: 'deimos', label: '准西北', children: [
                { value: 'phoboss', label: '哈浅217井' },
                { value: 'deimoss', label: '哈浅218井' },
            ],
        },
    ],
}];

class Widget extends React.Component {
    state = {
        checked: [],
        expanded: [],
    };

    render() {
        return (
            <CheckboxTree
                nodes={nodes}
                checked={this.state.checked}
                expanded={this.state.expanded}
                onCheck={checked => this.setState({ checked })}
                onExpand={expanded => this.setState({ expanded })}
                icons={{
                    check: <span className="rct-icon rct-icon-check" />,
                    uncheck: <span className="rct-icon rct-icon-uncheck" />,
                    halfCheck: <span className="rct-icon rct-icon-half-check" />,
                    expandClose: <span className="rct-icon rct-icon-expand-close" />,
                    expandOpen: <span className="rct-icon rct-icon-expand-open" />,
                    expandAll: <span className="rct-icon rct-icon-expand-all" />,
                    collapseAll: <span className="rct-icon rct-icon-collapse-all" />,
                    parentClose: <span className="rct-icon rct-icon-parent-close" />,
                    parentOpen: <span className="rct-icon rct-icon-parent-open" />,
                    leaf: <span className="rct-icon rct-icon-leaf" />,
                }}
            />
        );
    }
}

export default Widget;