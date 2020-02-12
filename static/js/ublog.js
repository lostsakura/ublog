/**
 * ublog通用js
 */

"use strict";

// 注销按钮被点击
$('.ublog-logout-btn').click(() => {
    $.post('/logout/', {}, (data) => {
        if (data['status'] === 'success') {
            Swal.fire({
                title: '您已成功注销',
                timer: 2000,
                showConfirmButton: false,
                onClose: () => {
                    $(window).attr('location','/');
                }
            });
        }
    });
    return false;
});

// 点击切换选项卡
function tagActive(tag) {
    $('.nav-link').removeClass('active');
    $('#' + tag).addClass('active');
}

// 切换父框架的选项卡
function parentTagActive(tag) {
    $('.nav-link', parent.document).removeClass('active');
   $("#" + tag, parent.document).addClass('active');
}