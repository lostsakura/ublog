"use strict";

$(() => {
    parentTagActive('ublog-tab-us');
});

// 重置密码
$('#recover-password-btn').click(() => {
    window.parent.location.href = '/recover-password/';
});

// 保存设置
function submitUserSettings() {
    let is_valid = $('#user-settings-form').valid();
    if (is_valid) {
        if (is_valid) {
            $.post('/admin/user-setup/', {
                userName: $('#us-username').val(),
                userId: $('#us-user-id').val()
            }, (data) => {
                if (data['status'] === 'success') {
                    window.parent.Swal.fire({
                        icon: 'success',
                        title: data['info'],
                        timer: 2000,
                        showConfirmButton: false,
                        onClose: () => {
                            self.parent.location.reload();
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
}