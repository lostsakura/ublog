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