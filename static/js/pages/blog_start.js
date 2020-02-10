"use strict";

// 获取邮箱验证码
$('#blog-start-get-verify-code').click(function () {

    const Toast = Swal.mixin({
                  toast: true,
                  position: 'top-end',
                  showConfirmButton: false,
                  timer: 3000
                });

    // 局部验证 - 验证邮箱
    let is_valid = $('#blog-start-form').validate().element($('#user-email'));
    if (is_valid) {
        console.log(123);
        $.post('/get-verify-code/', {
            userEmail: $('#user-email').val()
        }, function (data) {
            if (data['status'] === 'success') {
                Toast.fire({
                    type: 'success',
                    title: '邮件验证码发送成功'
                  })
            } else if (data['status'] === 'error') {
                Toast.fire({
                    type: 'error',
                    title: '邮件验证码发送失败'
                  })
            }
        });
    }
});


// 表单提交
$("#blog-start-submit").click(function () {
    // 验证表单
    let is_valid = $('#blog-start-form').valid();
    if (is_valid) {
        $.post('/start/', {
            userEmail: $('#user-email').val(),
            verifyCode: $('#verify-code').val(),
            userPassword: $('#user-password').val(),
            siteName: $('#site-name').val(),
            siteAddress: $('#site-address').val(),
            siteDesc: $('#site-desc').val(),
            siteKeyword: $('#site-keyword').val(),
            siteAllowComment: $('#site-allow-comment').val()
        }, function (data) {
            // 回调函数
            if (data['status'] === 'success') {
                Swal.fire({
                    position: 'center',
                    icon: 'success',
                    title: '初始化成功，正在跳转至后台管理',
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
                    type: 'error',
                    title: '初始化失败，请检查相应的配置'
                })
            }
        });
    }
});