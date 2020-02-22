"use strict";

// 获取当前url中的参数
function getQueryVariable(variable) {
    let query = window.location.search.substring(1);
    let vars = query.split("&");
    for (let i = 0; i < vars.length; i++) {
        let pair = vars[i].split("=");
        if (pair[0] === variable) {
            return pair[1];
        }
    }
    return false;
}

$(() => {
    parentTagActive('ublog-tab-wp');

    // Summernote
    $('#page-content').summernote({
        placeholder: '创作你的创作',
        tabsize: 2,
        height: 300
    });

    // 反显编辑器内容
    if (getQueryVariable('type') === 'update') {
        let psnc = $('#page-sn-content').html();
        $('#page-content').summernote('code', psnc);
    }
});

// #write-page-form

// 提交页面
function submitPage(type) {
    let is_valid = $('#write-page-form').valid();
    if (is_valid) {
        $.post('/admin/write-page/', {
            pageId: $('#page-id').val(),
            pageTitle: $('#page-title').val(),
            pageContent: $('#page-content').summernote('code'),
            pageSortId: $('#page-sort-id').val(),
            pageIsDraft: type
        }, (data) => {
            if (data['status'] === 'success') {
                window.parent.Swal.fire({
                    icon: 'success',
                    title: data['info'],
                    timer: 2000,
                    showConfirmButton: false,
                    onClose: () => {
                        $(window).attr('location', '/admin/manage-pages/');
                    }
                });
            } else if (data['status'] === 'error') {
                Swal.fire({
                    toast: true,
                    position: 'top-end',
                    icon: 'error',
                    title: '提交失败',
                    text: data['info'],
                    timer: 2600,
                    showConfirmButton: false,
                });
            }
        });
    }
}