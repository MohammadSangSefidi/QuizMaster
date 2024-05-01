from django.urls import path

from QuizModule.views import *

urlpatterns = [
    path('gotQuizes/', GotQuizes.as_view()),
    path('createQuiz/', CreateQuiz.as_view()),
    path('addQuestion/', AddQuestion.as_view()),
    path('filterQuizes/', FilterQuizes.as_view()),
    path('gotQuestions/', GotQuestions.as_view()),
    path('saveQuizPlayer/', SaveQuizPlayer.as_view()),
    path('checkQuizPlayers/', CheckQuizPlayers.as_view()),
]