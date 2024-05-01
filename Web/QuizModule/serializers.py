from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import QuizModel, QuestionsModel


class QuizSerializer(ModelSerializer):
    maker = serializers.SerializerMethodField()

    class Meta:
        model = QuizModel
        fields = [
            'id',
            'title',
            'quiz_class',
            'info',
            'score',
            'questions_count',
            'time',
            'maker',
            'quiz_code',
            'is_random',
            'random_count'
        ]

    def get_maker(self, obj):
        return obj.maker.username


class QuestionsSerializer(ModelSerializer):
    examId = serializers.SerializerMethodField()
    optionOne = serializers.SerializerMethodField(source='option_one')
    optionTwo = serializers.SerializerMethodField(source='option_two')
    optionThree = serializers.SerializerMethodField(source='option_three')
    optionFour = serializers.SerializerMethodField(source='option_four')

    class Meta:
        model = QuestionsModel
        fields = [
            'id',
            'question',
            'optionOne',
            'optionTwo',
            'optionThree',
            'optionFour',
            'anwser',
            'score',
            'examId'
        ]

    def get_examId(self, obj):
        return obj.quiz.id

    def get_optionOne(self, obj):
        return obj.option_one

    def get_optionThree(self, obj):
        return obj.option_three

    def get_optionFour(self, obj):
        return obj.option_two

    def get_optionTwo(self, obj):
        return obj.option_two