# Generated by Django 3.1.1 on 2023-12-17 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='syllabus',
        ),
        migrations.AddField(
            model_name='group',
            name='syllabus',
            field=models.ManyToManyField(to='main.Syllabus'),
        ),
    ]