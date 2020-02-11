/**
 * 用于验证ublog的所有form表单
 */

"use strict";

// 添加自定义jquery-validator验证规则
$.validator.addMethod(
    'emailVerifyCode',
    function (value, element, params) {
        if (params) {
            let flag = true;
            // 正则校验 右键验证码是否为6位数字
            let patrn = /^[0-9]{6}$/;
            flag = patrn.test(value);
            return flag;
        }
    }
);

// 添加确认密码的验证规则
$.validator.addMethod(
    'confirmPassword',
    function (value, element, params) {
        if (params) {
            if (value === $('#' + params).val()) {
                return true
            } else {
                return false
            }
        }
    }
);

$(document).ready(function () {

    // blog_start
    $('#blog-start-form').validate({
        rules: {
            userEmail: {
                required: true,
                email: true
            },
            userPassword: {
                required: true,
                minlength: 8,
                maxlength: 16
            },
            verifyCode: {
                required: true,
                emailVerifyCode: true
            },
            userName: {
                required: true,
                minlength: 4,
                maxlength: 20
            },
            siteName: {
                required: true
            },
            siteAddress: {
                url: true
            },
            siteKeyword: {
                required: true
            },
            siteAllowComment: {
                required: true
            },

        },
        messages: {
            userEmail: {
                required: "邮箱不能为空",
                email: "请输入格式正确的邮箱"
            },
            userPassword: {
                required: "密码不能为空",
                minlength: "密码最小长度不能少于8位",
                maxlength: "密码最大长度不能超过16位"
            },
            userName: {
                required: "用户名不能为空",
                minlength: "密码最小长度不能少于4位",
                maxlength: "密码最大长度不能超过20位"
            },
            verifyCode: {
                required: "验证码不能为空",
                emailVerifyCode: "请输入格式正确的验证码"
            },
            siteName: {
                required: "站点名称不能为空"
            },
            siteAddress: {
                url: "请输入合法的网址"
            },
            siteKeyword: {
                required: "站点关键词不能为空，例如：ublog,blog,我的博客 等"
            },
            siteAllowComment: {
                required: "必须选择"
            }
        },
        errorElement: 'span',
        errorPlacement: function (error, element) {
          error.addClass('invalid-feedback');
          element.closest('.form-group').append(error);
        },
        highlight: function (element, errorClass, validClass) {
          $(element).addClass('is-invalid');
        },
        unhighlight: function (element, errorClass, validClass) {
          $(element).removeClass('is-invalid');
        }
    });


    // blog_login
    $('#blog-login-form').validate({
        rules: {
            userName: {
                required: true,
                minlength: 4,
                maxlength: 20
            },
            userPassword: {
                required: true,
                minlength: 8,
                maxlength: 16
            }
        },
        messages: {
            userName: {
                required: "用户名不能为空",
                minlength: "密码最小长度不能少于4位",
                maxlength: "密码最大长度不能超过20位"
            },
            userPassword: {
                required: "密码不能为空",
                minlength: "密码最小长度不能少于8位",
                maxlength: "密码最大长度不能超过16位"
            }
        },
        errorElement: 'span',
        errorPlacement: function (error, element) {
          error.addClass('invalid-feedback');
          element.closest('.form-group').append(error);
        },
        highlight: function (element, errorClass, validClass) {
          $(element).addClass('is-invalid');
        },
        unhighlight: function (element, errorClass, validClass) {
          $(element).removeClass('is-invalid');
        }
    });


    // forgot_password
    $('#forgot-password-form').validate({
        rules: {
            userEmail: {
                required: true,
                email: true
            },
            verifyCode: {
                required: true,
                emailVerifyCode: true
            },
            newPassword: {
                required: true,
                minlength: 8,
                maxlength: 16
            },
            confirmNewPassword: {
                required: true,
                minlength: 8,
                maxlength: 16,
                confirmPassword: 'new-password'
            }
        },
        messages: {
            userEmail: {
                required: "邮箱不能为空",
                email: "请输入格式正确的邮箱"
            },
            verifyCode: {
                required: "验证码不能为空",
                emailVerifyCode: "请输入格式正确的验证码"
            },
            newPassword: {
                required: "密码不能为空",
                minlength: "密码最小长度不能少于8位",
                maxlength: "密码最大长度不能超过16位"
            },
            confirmNewPassword: {
                required: "密码不能为空",
                minlength: "密码最小长度不能少于8位",
                maxlength: "密码最大长度不能超过16位",
                confirmPassword: "密码不一致"
            }
        },
        errorElement: 'span',
        errorPlacement: function (error, element) {
          error.addClass('invalid-feedback');
          element.closest('.form-group').append(error);
        },
        highlight: function (element, errorClass, validClass) {
          $(element).addClass('is-invalid');
        },
        unhighlight: function (element, errorClass, validClass) {
          $(element).removeClass('is-invalid');
        }
    });
});


