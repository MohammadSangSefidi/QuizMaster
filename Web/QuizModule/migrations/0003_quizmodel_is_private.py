# Generated by Django 5.0.4 on 2024-04-24 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuizModule', '0002_quizplayersmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizmodel',
            name='is_private',
            field=models.BooleanField(default=False, verbose_name='شخصی هست/نیست'),
        ),
    ]
