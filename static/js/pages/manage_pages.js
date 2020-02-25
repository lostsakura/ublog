"use strict";

// 联动选项卡
$(() => {
    parentTagActive('ublog-tab-mp');
});

function deleteItems() {
    let delete_list = [];
    $.each($('.bp-checkbox:checked'), function () {
        delete_list.push($(this).val());
    });
    let delete_list_json = JSON.stringify(delete_list);

    window.parent.Swal.fire({
        icon: 'warning',
        title: '您确定要删除选中的页面么？',
        text: '删除之后不可恢复，请谨慎选择',
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        showCancelButton: true,
    }).then((result) => {
        if (result.value) {
            $.post('/admin/delete-resource/', {
                resourceType: 'blog_page',
                resourceId: delete_list_json
            }, (data) => {
                if (data['status'] === 'success') {
                    window.parent.Swal.fire({
                        icon: 'success',
                        title: data['info'],
                        timer: 1000,
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
                        title: data['info'],
                        timer: 2400,
                        showConfirmButton: false,
                    });
                }
            });
        }
    });
}