# Generated by Django 5.2 on 2025-04-23 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_delete_coursesubscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='used_temp_password',
            field=models.BooleanField(default=False),
        ),
    ]
