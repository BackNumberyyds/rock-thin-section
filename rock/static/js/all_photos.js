
document.addEventListener("DOMContentLoaded", function (event) {
    // 表单数据回显
    // const mines_selected = document.getElementById('id_mines_selected');
    // const lens_selected = document.getElementById('id_lens_selected');
    // const orths_selected = document.getElementById('id_orths_selected');
    // var mines_selected_list = mines_selected.value.split(',');
    // var lens_selected_list = lens_selected.value.split(',');
    // var orths_selected_list = orths_selected.value.split(',');

    // document.querySelectorAll('input[name="mines_checkboxs"]').forEach(mine => {
    //     if (mines_selected_list.includes(mine.value)) {
    //         mine.checked = true;
    //     }
    // });
    // document.querySelectorAll('input[name="lens_checkboxs"]').forEach(len => {
    //     if (lens_selected_list.includes(len.value)) {
    //         len.checked = true;
    //     }
    // });
    // document.querySelectorAll('input[name="orths_checkboxs"]').forEach(orth => {
    //     if (orths_selected_list.includes(orth.value)) {
    //         orth.checked = true;
    //     }
    // });

    const open = document.getElementById('open-menu');
    const close = document.getElementById('dismiss');
    var sidebar = document.getElementById('sidebar');
    var overlay = document.getElementById('overlay');

    // 打开侧边栏
    open.addEventListener('click', function () {
        sidebar.classList.add('active');
        overlay.classList.add('active');
    })

    // 关闭侧边栏
    close.addEventListener('click', function () {
        sidebar.classList.remove('active');
        overlay.classList.remove('active');
    })
    overlay.addEventListener('click', function () {
        sidebar.classList.remove('active');
        overlay.classList.remove('active');
    })

    // var mid_checkboxs = document.querySelectorAll('.mid-checkbox');
    // mid_checkboxs.forEach(function (parent_checkbox) {
    //     parent_checkbox.addEventListener('change', function () {
    //         if (this.checked) {
    //             this.nextElementSibling.nextElementSibling.querySelectorAll('input[type="checkbox"]').forEach(function (sub_checkbox) {
    //                 sub_checkbox.checked = true;
    //             })
    //             // 执行当复选框被选中时的操作
    //         } else {
    //             this.nextElementSibling.nextElementSibling.querySelectorAll('input[type="checkbox"]').forEach(function (sub_checkbox) {
    //                 sub_checkbox.checked = false;
    //             })
    //             // 执行当复选框被取消选中时的操作
    //         }
    //     });
    // });

    // const is_all_depth_checkbox = document.getElementById('is_all_depth');
    // const is_range_search_checkbox = document.getElementById('is_range_search');
    // const depth_low_input = document.getElementsByName('depth_low')[0];
    // const depth_high_input = document.getElementsByName('depth_high')[0];
    // is_all_depth_checkbox.addEventListener('change', function () {
    //     // 选中全部井深
    //     if (this.checked) {
    //         is_range_search_checkbox.checked = false;
    //         is_range_search_checkbox.disabled = true;
    //         depth_low_input.value = '';
    //         depth_high_input.value = '';
    //         depth_low_input.disabled = true;
    //         depth_high_input.disabled = true;
    //     } else {
    //         is_range_search_checkbox.disabled = false;
    //         depth_low_input.disabled = false;
    //     }
    // });
    // is_range_search_checkbox.addEventListener('change', function () {
    //     // 选中范围搜索
    //     if (this.checked) {
    //         depth_high_input.disabled = false;
    //     } else {
    //         depth_high_input.value = '';
    //         depth_high_input.disabled = true;
    //     }
    // });
});

function submitform() {
    const search_form = document.getElementById('search_form');
    const submit_botton = document.getElementById('search_form_submit_button');
    var alert_div = document.getElementById('alert_div');
    var alert_list = [];

    // 检测是否选中地区
    var mines_selected = Array.prototype.filter.call(document.querySelectorAll('[name="mines_checkboxs"]'), function (mine) {
        return mine.checked;
    });
    if (mines_selected.length == 0) {
        alert_list.push('地区');
    } else {
        let retstr = mines_selected.map(function (mine) {
            return mine.value;
        }).join(',');
        document.getElementById('id_mines_selected').value = retstr;
    }

    // 检测是否选中物镜倍数
    var lens_selected = Array.prototype.filter.call(document.querySelectorAll('[name="lens_checkboxs"]'), function (len) {
        return len.checked;
    });
    if (lens_selected.length == 0) {
        alert_list.push('物镜倍数');
    } else {
        let retstr = lens_selected.map(function (len) {
            return len.value;
        }).join(',');
        document.getElementById('id_lens_selected').value = retstr;
    }

    // 检测是否选中正交偏光
    var orths_selected = Array.prototype.filter.call(document.querySelectorAll('[name="orths_checkboxs"]'), function (len) {
        return len.checked;
    });
    if (orths_selected.length == 0) {
        alert_list.push('正交偏光');
    } else {
        let retstr = orths_selected.map(function (orth) {
            return orth.value;
        }).join(',');
        document.getElementById('id_orths_selected').value = retstr;
    }

    if (alert_list.length > 0) {
        alert_div.textContent = '请选择' + alert_list.join('、');
        alert_div.parentElement.hidden = false;
    } else {
        alert_div.parentElement.hidden = true;
        submit_botton.click();
    }
}