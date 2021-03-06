"use strict";

// 联动选项卡
$(() => {
    parentTagActive('ublog-tab-ma');
});

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

// 切换分类列表
function changeArticleListURL(action_type) {
    window.location.href = '/admin/manage-articles?list=' + action_type + '&page=1'
}

// 批量删除
function deleteItems() {
    let delete_list = [];
    $.each($('.ba-checkbox:checked'), function () {
        delete_list.push($(this).val());
    });
    let delete_list_json = JSON.stringify(delete_list);

    window.parent.Swal.fire({
        icon: 'warning',
        title: '您确定要删除选中的文章么？',
        text: '删除之后不可恢复，请谨慎选择',
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        showCancelButton: true,
    }).then((result) => {
        if (result.value) {
            $.post('/admin/delete-resource/', {
                resourceType: 'blog_article',
                resourceId: delete_list_json
            }, (data) => {
                if (data['status'] === 'success') {
                    window.parent.Swal.fire({
                        icon: 'success',
                        title: data['info'],
                        timer: 1000,
                        showConfirmButton: false,
                        onClose: () => {
                            $(window).attr('location',
                                '/admin/manage-articles?list=' + getQueryVariable('list') + '&page=1');
                        }
                    });
                } else if (data['status'] === 'error') {
                    Swal.fire({
                        toast: true,
                        position: 'top-end',
                        icon: 'error',
                        title: data['info'],
                        timer: 2400,
                        showConfirmButton: false,
                    });
                }
            });
        }
    });
}