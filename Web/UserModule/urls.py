from django.urls import path
from .views import *

urlpatterns = [
    path('createUser/', CreateUser.as_view()),
    path('checkUsername/', CheckUsername.as_view()),
    path('getUser/', GetUser.as_view()),
    path('updateEmailAndClass/', UpdateEmailAndClass.as_view()),
    path('updateUsername/', UpdateUsername.as_view()),
    path('updatePassword/', UpdatePassword.as_view()),
    path('updateScore/', UpdateScore.as_view()),
]