# Generated by Django 2.2.17 on 2021-02-14 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SNS', '0007_post_repliedby'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='repliedBy',
            new_name='replyTo',
        ),
    ]