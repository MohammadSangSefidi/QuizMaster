# Generated by Django 5.0.4 on 2024-04-25 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuizModule', '0005_quizmodel_is_random'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quizmodel',
            name='questions_count',
        ),
        migrations.AddField(
            model_name='quizmodel',
            name='random_count',
            field=models.IntegerField(null=True, verbose_name='تعداد سوالات شانسی'),
        ),
    ]
