/**
 * ublog通用js
 */

"use strict";

// 注销按钮被点击
$('.ublog-logout-btn').click(() => {
    $.post('/logout/', {}, (data) => {
        if (data['status'] === 'success') {
            Swal.fire({
                title: '您已成功注销',
                timer: 2000,
                showConfirmButton: false,
                onClose: () => {
                    $(window).attr('location', '/');
                }
            });
        }
    });
    return false;
});

// 点击切换选项卡
function tagActive(tag) {
    $('.nav-link').removeClass('active');
    $('#' + tag).addClass('active');
}

// 切换父框架的选项卡
function parentTagActive(tag) {
    $('.nav-link', parent.document).removeClass('active');
    $("#" + tag, parent.document).addClass('active');
}


// 提交评论
function submitComment() {
    let is_valid = $('#u-comment-form').valid();
    if (is_valid) {
        let article_id = $('.u-article-id').text();
        let comment_name = $('#u-bc-name').val();
        let comment_email = $('#u-bc-email').val();
        let comment_content = $('#u-bc-content').val();
        $.post('/submit-comment/', {
            articleId: article_id,
            commentName: comment_name,
            commentEmail: comment_email,
            commentContent: comment_content
        }, (data) => {
            if (data['status'] === 'success') {
                Swal.fire({
                    toast: true,
                    position: 'center',
                    icon: 'success',
                    title: '提交成功',
                    text: data['info'],
                    timer: 3000,
                    showConfirmButton: false,
                    onClose: () => {
                        location.reload();
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