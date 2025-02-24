# Generated by Django 5.1.6 on 2025-02-24 07:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_employee_task_assigned_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskdetail',
            name='task',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='tasks.task'),
        ),
    ]
