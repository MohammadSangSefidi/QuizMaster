from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from Web.authentications import CustomTokenAuthentication
from .models import UserModel
from .serializers import UserSerializer


# Create your views here.


class CreateUser(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'get is not allowed'})

    def post(self, request):
        data = UserSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
            userName = data.validated_data['username']
            password = data.validated_data['password']
            teacher = request.data['teacher']
            if teacher:
                name = data.validated_data['first_name']
                lastName = data.validated_data['last_name']
                email = data.validated_data['email']
                user = UserModel(username=userName, first_name=name, last_name=lastName, profile_image=1,email=email, isTeacher=teacher)
                user.set_password(password)
                user.save()
            else:
                user = UserModel(username=userName, profile_image=1, isTeacher=teacher)
                user.set_password(password)
                user.save()
            return Response({'message': 'success'})
        else:
            return Response({'message': 'data is not valid'})


class CheckUsername(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.data['username']
        user = UserModel.objects.filter(username=username).first()
        if user is not None:
            return Response({'message': False})
        else:
            return Response({'message': True})

    def post(self, request):
        return Response({'message': 'post is not allowed'})


class GetUser(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.data['username']
        password = request.data['password']
        user = UserModel.objects.filter(username=username).first()
        if user is not None:
            if user.check_password(password):
                return Response({'message': {'id': user.id, 'userName': user.username, 'password': user.password,
                                             'score': user.score, 'class': user.user_class, 'email': user.email,
                                             'profileImage': user.profile_image, 'isTeacher': user.isTeacher}})
            else:
                return Response({'message': None})
        else:
            return Response({'message': None})

    def post(self, request):
        return Response({'message': 'post is not allowed'})


class UpdateEmailAndClass(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'get is not allowed'})

    def post(self, request):
        data = request.data
        userName = data['username']
        newEmail = data['newEmail']
        newClass = data['newClass']
        if userName is not None and newClass is not None and newEmail is not None:
            user = UserModel.objects.filter(username=userName).first()
            if user is not None:
                user.email = newEmail
                user.user_class = newClass
                user.save()
                return Response({'message': 'success'})
            else:
                return Response({'message': 'username is not valid'})
        else:
            return Response({'message': 'data is not valid'})


class UpdateProfileImage(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'get is not allowed'})

    def post(self, request):
        data = request.data
        userName = data['username']
        newImage = data['image']
        if userName is not None and newImage is not None:
            user = UserModel.objects.filter(username=userName).first()
            if user is not None:
                user.profile_image = int(newImage)
                user.save()
                return Response({'message': 'success'})
            else:
                return Response({'message': 'username is not valid'})
        else:
            return Response({'message': 'data is not valid'})


class UpdateUsername(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'get is not allowed'})

    def post(self, request):
        data = request.data
        userName = data['username']
        newUserName = data['newUsername']
        if userName is not None and newUserName is not None:
            user = UserModel.objects.filter(username=userName).first()
            if user is not None:
                user.username = newUserName
                user.save()
                return Response({'message': 'success'})
            else:
                return Response({'message': 'username is not valid'})
        else:
            return Response({'message': 'data is not valid'})


class UpdatePassword(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'get is not allowed'})

    def post(self, request):
        data = request.data
        userName = data['username']
        newPassword = data['newPassword']
        if userName is not None and newPassword is not None:
            user = UserModel.objects.filter(username=userName).first()
            if user is not None:
                user.set_password(newPassword)
                user.save()
                return Response({'message': 'success'})
            else:
                return Response({'message': 'username is not valid'})
        else:
            return Response({'message': 'data is not valid'})


class UpdateScore(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'get is not allowed'})

    def post(self, request):
        id = request.data['id']
        score = request.data['score']
        user = UserModel.objects.filter(id=id).first()
        if user is not None:
            if type(score) == int and int(score) > 0:
                user.score = user.score + score
                user.save()
                return Response({'message': 'success'})
            else:
                return Response({'message': 'score is not valid'})
        else:
            return Response({'message': 'user id is not valid'})


class GetLeaderBoard(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = UserModel.objects.filter(isTeacher=False).order_by('-score')[:20]
        query = []
        for user in data:
            query.append({'username': user.username, 'score': user.score, 'image': user.profile_image})
        return Response({'message': query})

    def post(self, request):
        return Response({'message': 'post is not allowed'})