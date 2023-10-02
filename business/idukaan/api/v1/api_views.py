from django.contrib.auth.mixins import PermissionRequiredMixin

from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from knox.auth import TokenAuthentication

from business import models as BMdl
from business import serializers as BSrl
from business import permissions as BPerm
from business.idukaan.api.v1 import api_msg as BApiV1Msg

from users import models as UserMdl
from users import serializers as UserSrl
from users import permissions as UserPerm


'''
PROD
1. OrgTypesApi
2. OrgApi
3. OrgEmpApi
4. OrgStateGstApi
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


class OrgTypesApi(generics.ListAPIView, PermissionRequiredMixin):
    queryset = BMdl.OrgType.objects.all()
    serializer_class = BSrl.OrgTypesSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, UserPerm.IsVerified]
    

class OrgApi(viewsets.ViewSet, PermissionRequiredMixin):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, UserPerm.IsVerified]

    def create(self, request, *args, **kwargs):
        response_data = {}
        serializer = BSrl.AddOrgSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            response_data['org'] = serializer.data
            response_data['message'] = BApiV1Msg.AddOrgMsg.addOrgSuccess()
            return response_201(response_data)
        if serializer.errors['reg_no'][0].code == 'unique':
            return response_409(BApiV1Msg.AddOrgMsg.addOrgFoundFailed())
        return response_400(serializer.errors)
    
    def list(self, request, *args, **kwargs):
        response_data = {}
        queryset = request.user.orgemp_set.all()
        if queryset.count() > 0:
            orgs = []
            for org in queryset:
                orgs.append(BSrl.OrgListSerializer(org.org).data)
            response_data['org_list'] = orgs
            response_data['is_verified_msg'] = BApiV1Msg.OrgListMsg.orgVerificationInProcess()
            return Response(response_data, status=status.HTTP_200_OK)
        return response_400(BApiV1Msg.OrgListMsg.orgListFailed_NotFound())
