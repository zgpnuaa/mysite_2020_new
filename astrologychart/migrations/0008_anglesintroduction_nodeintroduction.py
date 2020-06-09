# Generated by Django 2.1.7 on 2019-10-26 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('astrologychart', '0007_auto_20191023_1912'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnglesIntroduction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('angle', models.CharField(max_length=30, verbose_name='基本点')),
                ('introduction', models.TextField(verbose_name='介绍')),
            ],
            options={
                'verbose_name': '基本点介绍',
                'verbose_name_plural': '基本点介绍',
            },
        ),
        migrations.CreateModel(
            name='NodeIntroduction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('node', models.CharField(max_length=30, verbose_name='月亮南北交点')),
                ('introduction', models.TextField(verbose_name='介绍')),
            ],
            options={
                'verbose_name': '月亮南北交点介绍',
                'verbose_name_plural': '月亮南北交点介绍',
            },
        ),
    ]
