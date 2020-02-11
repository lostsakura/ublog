"use strict";

// 获取验证码
$('#forgot-password-get-verify-code').click(function () {
    let is_valid = $('#forgot-password-form').validate().element($('#user-email'));
    if (is_valid) {
        $.post('/get-verify-code/', {
            userEmail: $('#user-email').val(),
            type: '1'
        }, function (data) {
            if (data['status'] === 'success') {
                Swal.fire({
                    toast: true,
                    position: 'top-end',
                    showConfirmButton: false,
                    timer: 3000,
                    icon: 'success',
                    title: data['info']
                })
            } else if (data['status'] === 'error') {
                Swal.fire({
                    toast: true,
                    position: 'top-end',
                    showConfirmButton: false,
                    timer: 3000,
                    icon: 'error',
                    title: data['info']
                })
            }
        });
    }
});

// 提交重置密码表单
$('#forgot-password-submit').click(function () {
    let is_valid = $('#forgot-password-form').valid();
    if (is_valid) {
        $.post('/forgot-password/', {
            userEmail: $('#user-email').val(),
            verifyCode: $('#verify-code').val(),
            newPassword: $('#confirm-new-password').val()
        }, function (data) {
            if (data['status'] === 'success') {
                Swal.fire({
                    icon: 'success',
                    title: '重置密码成功',
                    text: data['info'],
                    onClose: () => {
                        $(window).attr('location','/login/');
                    }
                })
            } else if (data['status'] === 'error') {
                Swal.fire({
                    toast: true,
                    position: 'top-end',
                    showConfirmButton: false,
                    timer: 3000,
                    icon: 'error',
                    title: data['info']
                })
            }
        });
    }
});