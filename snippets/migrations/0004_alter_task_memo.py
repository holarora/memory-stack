# Generated by Django 5.0.6 on 2024-07-12 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0003_task_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='memo',
            field=models.TextField(max_length=200, null=True, verbose_name='メモの追加'),
        ),
    ]
