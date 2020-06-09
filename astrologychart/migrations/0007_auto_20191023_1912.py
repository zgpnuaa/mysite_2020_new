# Generated by Django 2.1.7 on 2019-10-23 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('astrologychart', '0006_auto_20191020_1459'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ascsign',
            old_name='sign_asc',
            new_name='sign',
        ),
        migrations.RenameField(
            model_name='chironsign',
            old_name='sign_chiron',
            new_name='sign',
        ),
        migrations.RenameField(
            model_name='dessign',
            old_name='sign_des',
            new_name='sign',
        ),
        migrations.RenameField(
            model_name='icsign',
            old_name='sign_ic',
            new_name='sign',
        ),
        migrations.RenameField(
            model_name='jupitersign',
            old_name='sign_jupiter',
            new_name='sign',
        ),
        migrations.RenameField(
            model_name='marssign',
            old_name='sign_mars',
            new_name='sign',
        ),
        migrations.RenameField(
            model_name='mcsign',
            old_name='sign_mc',
            new_name='sign',
        ),
        migrations.RenameField(
            model_name='mercurysign',
            old_name='sign_mercury',
            new_name='sign',
        ),
        migrations.RenameField(
            model_name='moonsign',
            old_name='sign_moon',
            new_name='sign',
        ),
        migrations.RenameField(
            model_name='neptunesign',
            old_name='sign_neptune',
            new_name='sign',
        ),
        migrations.RenameField(
            model_name='nnodesign',
            old_name='sign_nnode',
            new_name='sign',
        ),
        migrations.RenameField(
            model_name='plutosign',
            old_name='sign_pluto',
            new_name='sign',
        ),
        migrations.RenameField(
            model_name='saturnsign',
            old_name='sign_saturn',
            new_name='sign',
        ),
        migrations.RenameField(
            model_name='snodesign',
            old_name='sign_snode',
            new_name='sign',
        ),
        migrations.RenameField(
            model_name='sunsign',
            old_name='sign_sun',
            new_name='sign',
        ),
        migrations.RenameField(
            model_name='uranussign',
            old_name='sign_uranus',
            new_name='sign',
        ),
        migrations.RenameField(
            model_name='venussign',
            old_name='sign_venus',
            new_name='sign',
        ),
    ]
