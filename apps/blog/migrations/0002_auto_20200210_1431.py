# Generated by Django 2.2 on 2020-02-10 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogsettings',
            name='allow_comment',
            field=models.BooleanField(choices=[(False, '禁止评论'), (True, '可以评论')], default=False, verbose_name='是否可以评论'),
        ),
    ]