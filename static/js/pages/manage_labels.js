"use strict";

// 联动选项卡
$(() => {
    parentTagActive('ublog-tab-ml');
});

// 获取当前url中的参数
function getQueryVariable(variable)
{
   let query = window.location.search.substring(1);
   let vars = query.split("&");
   for (let i=0;i<vars.length;i++) {
           let pair = vars[i].split("=");
           if(pair[0] === variable){return pair[1];}
   }
   return false;
}

// 提交按钮
$('#admin-manage-labels-submit').click(() => {
    let is_valid = $('#admin-manage-labels-form').valid();
    let page_num = getQueryVariable('page');
    if (is_valid) {
        $.post('/admin/manage-labels/', {
            labelName: $('#label-name').val(),
            labelId: $("#label-id").val()
        }, (data) => {
            if (data['status'] === 'success') {
                window.parent.Swal.fire({
                    icon: 'success',
                    title: data['info'],
                    timer: 1600,
                    showConfirmButton: false,
                    onClose: () => {
                        $(window).attr('location', '/admin/manage-labels?type=list&page=' + page_num);
                    }
                });
            } else if (data['status'] === 'error') {
                Swal.fire({
                    toast: true,
                    position: 'top-end',
                    icon: 'error',
                    title: data['info'],
                    timer: 3000,
                    showConfirmButton: false,
                });
            }
        });
    }
});

// 删除按钮
$('#admin-manage-labels-delete').click(() => {
    window.parent.Swal.fire({
        icon: 'warning',
        title: '您确定要删除么？',
        text: '删除之后可以重新添加',
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        showCancelButton: true,
    }).then((result) => {
        if (result.value) {
            let page_num = getQueryVariable('page');
            $.post('/admin/delete-resource/', {
                resourceType: 'blog_label',
                resourceId: $("#label-id").val()
            }, (data) => {
                if (data['status'] === 'success') {
                    window.parent.Swal.fire({
                        icon: 'success',
                        title: data['info'],
                        timer: 1000,
                        showConfirmButton: false,
                        onClose: () => {
                            $(window).attr('location', '/admin/manage-labels?type=list&page=' + page_num);
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
});