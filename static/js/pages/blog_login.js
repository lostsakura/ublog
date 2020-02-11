"use strict";

// 登陆按钮
$('#blog-login-submit').click(function () {
    let is_valid = $('#blog-login-form').valid();
    let is_rm = '0';
    if ($('#remember-me').is(':checked')) {
        is_rm = '1'
    }
    if (is_valid) {
        $.post('/login/',{
            userName: $('#user-name').val(),
            userPassword: $('#user-password').val(),
            rememberMe : is_rm
        }, function (data) {
            if (data['status'] === 'success') {
                Swal.fire({
                    icon: 'success',
                    title: '登陆成功',
                    text: data['info'],
                    timer: 2000,
                    showConfirmButton: false,
                    onClose: () => {
                        $(window).attr('location','/admin/');
                    }
                });
            } else if (data['status'] === 'error') {
                Swal.fire({
                    toast: true,
                    position: 'top-end',
                    showConfirmButton: false,
                    timer: 3000,
                    icon: 'error',
                    title: '登陆失败',
                    text: data['info']
                })
            }
        })
    }
});