from rest_framework import status, generics
from rest_framework.response import Response


from users import models as UserMdl
from users import serializers as UserSrl


'''
# Prod
# Dev
1.UserSignupApi
'''

class UserSignupApi(generics.CreateAPIView):
    serializer_class = UserSrl.UserSignupSerializer

    def post(self, request, *args, **kwargs):
        response_data = {}
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'user' : serializer.data,
                'message' : 'We are happy to on-board you. Please check registered  mail for account verification link and instructions to verify identity.'
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        response_data = serializer.errors
        response_data['message'] = "We're sorry, but we couldn't sign you up. Please check your information and try again."
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
