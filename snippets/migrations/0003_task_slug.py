# Generated by Django 5.0.6 on 2024-07-09 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0002_task_duedate_task_step_alter_task_memo'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='slug',
            field=models.SlugField(default=''),
        ),
    ]
