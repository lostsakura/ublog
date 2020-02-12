from django.contrib import admin

# Register your models here.

from blog.models import ArticleComment, BlogLabel, BlogArticle, BlogUser, BlogSettings

admin.site.register(ArticleComment)
admin.site.register(BlogLabel)
admin.site.register(BlogArticle)
admin.site.register(BlogUser)
admin.site.register(BlogSettings)
