"use strict";

$(() => {
    parentTagActive('ublog-tab-ss');
});


// 提交系统设置
function submitSystemSettings() {
    let is_valid = $('#system-settings-form').valid();
    if (is_valid) {
        $.post('/admin/system-setup/', {
            siteId: $('#ss-bs-id').val(),
            siteName: $('#ss-site-name').val(),
            siteAddress: $('#ss-site-address').val(),
            siteDesc: $('#ss-site-desc').val(),
            siteKeyword: $('#ss-site-keyword').val(),
            siteAllowComment: $('#ss-allow-comment').val()
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
        })
    }
}
