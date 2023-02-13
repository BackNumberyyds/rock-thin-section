
document.addEventListener("DOMContentLoaded", function (event) {
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

    var mid_checkboxs = document.querySelectorAll('.mid-checkbox');
    mid_checkboxs.forEach(function (parent_checkbox) {
        parent_checkbox.addEventListener('change', function () {
            if (this.checked) {
                this.nextElementSibling.nextElementSibling.querySelectorAll('input[type="checkbox"]').forEach(function (sub_checkbox) {
                    sub_checkbox.checked = true;
                })
                // 执行当复选框被选中时的操作
            } else {
                this.nextElementSibling.nextElementSibling.querySelectorAll('input[type="checkbox"]').forEach(function (sub_checkbox) {
                    sub_checkbox.checked = false;
                })
                // 执行当复选框被取消选中时的操作
            }
        });
    });

    const is_all_depth_checkbox = document.getElementById('is_all_depth');
    const is_range_search_checkbox = document.getElementById('is_range_search');
    const depth_low_input = document.getElementsByName('depth_low')[0];
    const depth_high_input = document.getElementsByName('depth_high')[0];
    is_all_depth_checkbox.addEventListener('change', function () {
        if (this.checked) {
            is_range_search_checkbox.checked = false;
            is_range_search_checkbox.disabled = true;
            depth_low_input.value = '';
            depth_high_input.value = '';
            depth_low_input.disabled = true;
            depth_high_input.disabled = true;
        } else {
            is_range_search_checkbox.disabled = false;
            depth_low_input.disabled = false;
        }
    });
    is_range_search_checkbox.addEventListener('change', function () {
        if (this.checked) {
            depth_high_input.disabled = false;
        } else {
            depth_high_input.value = '';
            depth_high_input.disabled = true;
        }
    });

});