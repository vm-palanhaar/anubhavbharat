from django.contrib.auth import login

from rest_framework import status, generics
from rest_framework.response import Response

from knox.models import AuthToken

from users import models as UserMdl
from users import serializers as UserSrl
from users.common.api.v1 import api_msg as UserApiV1Msg


'''
# Prod
1.UserSignupApi
2. UserLoginApi
# Dev
'''

def response_200(response_data):
    return Response(response_data, status=status.HTTP_200_OK)

def response_201(response_data):
    return Response(response_data, status=status.HTTP_201_CREATED)

def response_400(response_data):
    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

def response_401(response_data):
    return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)

def response_403(response_data):
    return Response(response_data, status=status.HTTP_403_FORBIDDEN)

def response_409(response_data):
    return Response(response_data, status=status.HTTP_409_CONFLICT)

class UserSignupApi(generics.CreateAPIView):
    serializer_class = UserSrl.UserSignupSerializer

    def post(self, request, *args, **kwargs):
        response_data = {}
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            #TODO: Send email verification to user
            response_data = {
                'user' : serializer.data,
                'message' : UserApiV1Msg.UserSignUpMsg.userSignupSuccess()
            }
            return response_201(response_data)
        response_data = serializer.errors
        response_data['message'] = UserApiV1Msg.UserSignUpMsg.userSignupFailed()
        return response_400(response_data)


class UserLoginApi(generics.GenericAPIView):
    serializer_class = UserSrl.UserLoginSerializer

    def post(self, request, *args, **kwargs):
        response_data = {}
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            user = serializer.validated_data
            if type(user) is not UserMdl.User:
                try:
                    user = UserMdl.User.objects.get(username = request.data['username'])
                except UserMdl.User.DoesNotExist:
                    response_data['message'] = UserApiV1Msg.UserLoginMsg.userLoginFailed_UserCredInvalid()
                    return response_400(response_data)
                if user.is_active != True:
                    #TODO: Send email verification to user
                    response_data['message'] = UserApiV1Msg.UserLoginMsg.userLoginFailed_UserInActive()
                    return response_403(response_data)
            else:
                login(request, user)
                response_data['user'] = serializer.data
                response_data['token'] = AuthToken.objects.create(user)[1]
                response_data['message'] = UserApiV1Msg.UserLoginMsg.userLoginSuccess() if user.is_verified \
                    else UserApiV1Msg.UserLoginMsg.userLoginSuccess_UserInVerfieid()
                return response_201(response_data)
        response_data = serializer.errors
        response_data['message'] = UserApiV1Msg.UserLoginMsg.userLoginFailed_UserCredInvalid()
        return response_400(response_data)
