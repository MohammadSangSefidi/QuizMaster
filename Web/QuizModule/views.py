from django.db.models import Q
from django.shortcuts import render

# Create your views here.
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
        data = QuizSerializer(QuizModel.objects.all(), many=True).data
        return Response(data)

    def post(self, request):
        return Response({'message': 'post is not allowed'})


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
            if type(score) == int and int(score) > 0:
                result = QuizPlayersModel(user=user, quiz=quiz, score=score)
                result.save()
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