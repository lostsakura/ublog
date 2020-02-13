$(function () {
    // Summernote
    $('#article-content').summernote({
        placeholder: '创作你的创作',
        tabsize: 2,
        height: 300
    });
});

// 提交文章
function submitArticle(type) {
    let is_valid = $('#write-article-form').valid();
    if (is_valid) {
        $.post('/admin/write-article/', {
            articleTitle: $('#article-title').val(),
            articleContent: $('#article-content').summernote('code'),
            articleIsPrivate: $('#article-is-private').val(),
            articleLabel: $('#article-label').val(),
            articleId: $('#article-id').val(),
            articleIsDraft: type
        }, (data) => {
            if (data['status'] === 'success') {
                window.parent.Swal.fire({
                    icon: 'success',
                    title: data['info'],
                    timer: 2000,
                    showConfirmButton: false,
                    onClose: () => {
                        $(window).attr('location', '/admin/admin-index/');
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


