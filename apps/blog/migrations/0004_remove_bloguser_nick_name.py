# Generated by Django 2.2 on 2020-02-11 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20200210_1451'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bloguser',
            name='nick_name',
        ),
    ]