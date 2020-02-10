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

// blog_start
$(document).ready(function () {
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
});