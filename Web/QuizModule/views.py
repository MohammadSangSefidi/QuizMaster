from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from django.utils.crypto import get_random_string
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from QuizModule.models import QuizModel, QuestionsModel, QuizPlayersModel
from UserModule.models import UserModel
from Web.authentications import CustomTokenAuthentication
from .serializers import QuizSerializer, QuestionsSerializer


class GotQuizes(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        teacherId = request.data['teacherId']
        if teacherId is None:
            quizes = QuizSerializer(QuizModel.objects.filter(is_delete=False, is_private=False), many=True).data
            return Response(quizes)
        else:
            quizes = QuizSerializer(QuizModel.objects.filter(maker_id=teacherId, is_delete=False), many=True).data
            return Response(quizes)

    def post(self, request):
        return Response({'message': 'post is not allowed'})


class CreateQuiz(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'get is not allowed'})

    def post(self, request):
        id = request.data['teacherId']
        data = QuizSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
            title = data.validated_data['title']
            quiz_class = data.validated_data['quiz_class']
            info = data.validated_data['info']
            time = data.validated_data['time']
            is_random = data.validated_data['is_random']
            random_count = data.validated_data['random_count']
            newQuiz = QuizModel(title=title, quiz_class=quiz_class, info=info, time=time, is_random=is_random, random_count=random_count, is_private=True, quiz_code=get_random_string(10))
            user = UserModel.objects.filter(id=id).first()
            newQuiz.maker = user
            newQuiz.save()
            return Response({'message': 'accept', 'id': newQuiz.id})
        else:
            return Response(data)


class AddQuestion(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'get is not allowed'})

    def post(self, request):
        quizId = request.data['examId']
        questionText = request.data['question']
        optionOne = request.data['optionOne']
        optionTwo = request.data['optionTwo']
        optionThree = request.data['optionThree']
        optionFour = request.data['optionFour']
        anwser = request.data['anwser']
        score = request.data['score']
        newQuestion = QuestionsModel(question=questionText, option_one=optionOne, option_two=optionTwo, option_three=optionThree, option_four=optionFour, anwser=anwser, score=score)
        quize = QuizModel.objects.filter(id=quizId).first()
        newQuestion.quiz = quize
        newQuestion.save()
        return Response({'message': 'accept'})



class FilterQuizes(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        value = request.data['value']
        quizClass = request.data['class']
        if quizClass == 'هیچ کدام':
            if value == '':
                query = QuizModel.objects.all()
                quizes = QuizSerializer(query, many=True).data
                return Response(quizes)
            else:
                query = QuizModel.objects.filter(Q(title__contains=value) | Q(info__contains=value) | Q(maker__username__contains=value))
                quizes = QuizSerializer(query, many=True).data
                return Response(quizes)
        else:
            if value == '':
                query = QuizModel.objects.filter(quiz_class=quizClass)
                quizes = QuizSerializer(query, many=True).data
                return Response(quizes)
            else:
                query = QuizModel.objects.filter((Q(title__contains=value) | Q(info__contains=value) | Q(maker__username__contains=value)) & Q(quiz_class=quizClass))
                quizes = QuizSerializer(query, many=True).data
                return Response(quizes)

    def post(self, request):
        return Response({'message': 'post is not allowed'})


class GotQuestions(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        id = request.data['id']
        data = QuestionsSerializer(QuestionsModel.objects.filter(quiz_id=id), many=True).data
        if data is not None:
            return Response(data)
        else:
            return Response({'message': 'id is not valid'})

    def post(self, request):
        return Response({'message': 'post is not allowed'})


class SaveQuizPlayer(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'get is not allowed'})

    def post(self, request):
        userId = request.data['userId']
        exameId = request.data['exameId']
        score = request.data['score']
        user = UserModel.objects.filter(id=userId).first()
        quiz = QuizModel.objects.filter(id=exameId).first()
        if user is not None and quiz is not None:
            if type(score) == int and int(score) >= 0:
                result, isCreate = QuizPlayersModel.objects.get_or_create(user=user, quiz=quiz, score=score)
                return Response({'message': 'success'})
            else:
                return Response({'message': 'score is not valid'})
        else:
            return Response({'message': 'user or quiz id is not valid'})


class CheckQuizPlayers(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'get is not allowed'})

    def post(self, request):
        userId = request.data['userId']
        exameId = request.data['exameId']
        user = UserModel.objects.filter(id=userId).first()
        quiz = QuizModel.objects.filter(id=exameId).first()
        if user is not None and quiz is not None:
            result = QuizPlayersModel.objects.filter(user=user, quiz=quiz).first()
            if result is not None:
                return Response({'message': True})
            else:
                return Response({'message': False})
        else:
            return Response({'message': 'user or quiz id is not valid'})