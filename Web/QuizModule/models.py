from django.db import models
from UserModule.models import UserModel
# Create your models here.


class QuizModel(models.Model):
    title = models.CharField(max_length=50, verbose_name='عنوان')
    quiz_class = models.CharField(max_length=30, verbose_name='کلاس')
    info = models.TextField(verbose_name='توضیحات')
    score = models.IntegerField(verbose_name='امتیاز آزمون')
    questions_count = models.IntegerField(verbose_name='مجموع سوالات')
    time = models.IntegerField(verbose_name='زمان آزمون به دقیقه')
    maker = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='طراح آزمون')

    def __str__(self):
        return f'{self.title}:{self.maker.username}'


class QuestionsModel(models.Model):
    question = models.TextField(verbose_name='متن سوال')
    option_one = models.TextField(verbose_name='گزینه یک')
    option_two = models.TextField(verbose_name='گزینه دوم')
    option_three = models.TextField(verbose_name='گزینه سوم')
    option_four = models.TextField(verbose_name='گزینه چهارم')
    anwser = models.IntegerField(verbose_name='گزینه درست')
    score = models.IntegerField(verbose_name='امتیاز')
    quiz = models.ForeignKey(QuizModel, on_delete=models.CASCADE, verbose_name='آزمون')


class QuizPlayersModel(models.Model):
    quiz = models.ForeignKey(QuizModel, on_delete=models.CASCADE, verbose_name='آزمون')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='کاربر')
    score = models.IntegerField(verbose_name='امتیاز بدست آمده')