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
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
