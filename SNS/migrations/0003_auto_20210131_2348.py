# Generated by Django 2.2.17 on 2021-01-31 14:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SNS', '0002_post'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='created_date',
            new_name='pub_date',
        ),
    ]
