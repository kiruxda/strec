# Generated by Django 3.1.1 on 2023-12-17 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20231217_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='syllabus',
            name='course',
            field=models.IntegerField(default=1, verbose_name='Расписание на курс'),
        ),
    ]