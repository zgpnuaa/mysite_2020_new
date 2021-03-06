# Generated by Django 2.1.7 on 2020-05-07 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0005_articlepost_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='processstaterecord',
            name='completed',
            field=models.BooleanField(default=False, verbose_name='是否完结'),
        ),
        migrations.AlterField(
            model_name='processstaterecord',
            name='this_step_state',
            field=models.IntegerField(default=0, help_text='0：草稿；1：审批中；2：已发布；3：被驳回；4：已撤回；5：已删除', verbose_name='当前状态'),
        ),
    ]
