# Generated by Django 2.2.2 on 2019-06-22 13:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_course_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courses_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lesson', to='course.Course'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lesson_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
