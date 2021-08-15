# Generated by Django 2.2.16 on 2021-08-15 13:01

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='created',
            new_name='pub_date',
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('title', 'author')},
        ),
    ]
