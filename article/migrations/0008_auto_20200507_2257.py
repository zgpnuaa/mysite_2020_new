# Generated by Django 2.1.7 on 2020-05-07 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0007_remove_processstaterecord_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processstaterecord',
            name='process',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='state_process', to='article.ArticleProcessFlow', verbose_name='流程'),
        ),
    ]
