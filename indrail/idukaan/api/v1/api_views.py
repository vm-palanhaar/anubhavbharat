from django.contrib.auth.mixins import PermissionRequiredMixin

from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from knox.auth import TokenAuthentication

from tourism import api_errors as TErr

from indrail import models as IrMdl
from indrail import serializers as IrSrl
from indrail.idukaan.api.v1 import api_msg as IrApiV1Msg

from business import models as BMdl
from business.idukaan.api.v1 import api_msg as BApiV1Msg

from users import models as UserMdl
from users import permissions as UserPerm
from users.common.api.v1 import api_msg as UserApiV1Msg

'''
PROD
DEV
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


class ShopApi(viewsets.ViewSet, PermissionRequiredMixin):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, UserPerm.IsVerified]

    def create(self, request, *args, **kwargs):
        response_data = {}
        response_data['org_id'] = kwargs['orgId']
        if kwargs['orgId'] == str(request.data['org']):
            pass
        pass

    def list(self, request, *args, **kwargs):
        pass

    def partial_update(self, request, *args, **kwargs):
        pass
