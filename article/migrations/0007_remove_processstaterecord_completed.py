# Generated by Django 2.1.7 on 2020-05-07 14:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_auto_20200507_2242'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='processstaterecord',
            name='completed',
        ),
    ]
