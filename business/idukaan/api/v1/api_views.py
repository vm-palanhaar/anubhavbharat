from django.contrib.auth.mixins import PermissionRequiredMixin

from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from knox.auth import TokenAuthentication

from tourism import api_errors as TErr

from business import models as BMdl
from business import serializers as BSrl
from business import permissions as BPerm
from business.idukaan.api.v1 import api_msg as BApiV1Msg

from users import models as UserMdl
from users import serializers as UserSrl
from users import permissions as UserPerm
from users.common.api.v1 import api_msg as UserApiV1Msg


'''
PROD
1. OrgTypesApi
2. OrgApi
3. OrgEmpApi
4. OrgStateGstApi
DEV
'''

def validateOrgEmpObj(user, org):
        try:
            return BMdl.OrgEmp.objects.get(user=user, org=org)
        except BMdl.OrgEmp.DoesNotExist:
            return None
        
def validateOrgObj(org):
    return org.is_active and org.is_verified
        

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
        if 'reg_no' in serializer.errors and serializer.errors['reg_no'][0].code == 'unique':
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

    def retrieve(self, request, *args, **kwargs):
        org_emp = validateOrgEmpObj(user=request.user, org=kwargs['orgId'])
        if org_emp != None:
            serializer = BSrl.OrgInfoSerializer(org_emp.org)
            return response_200(serializer.data)
        return response_403(BApiV1Msg.businessOrgEmpSelfNotFound())


class OrgEmpApi(viewsets.ViewSet, PermissionRequiredMixin):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, UserPerm.IsVerified]

    def create(self, request, *args, **kwargs):
        response_data = {}
        response_data['org_id'] = kwargs['orgId']
        # validate org_id from URI and request body
        if kwargs['orgId'] == request.data['org']:
            org_emp = validateOrgEmpObj(user=request.user, org=kwargs['orgId'])
            # org is active and verified & employee is manager of the org
            if org_emp != None and validateOrgObj(org=org_emp.org) and org_emp.is_manager:
                # check the requested user exists in users profile
                try:
                    user = UserMdl.User.objects.get(username = request.data['user'])
                except UserMdl.User.DoesNotExist:
                    response_data.update(UserApiV1Msg.usernameUserNotFound())
                    return response_400(response_data)
                if user.is_active == False and user.is_verified == False:
                    response_data.update(UserApiV1Msg.userInActiveNotVerified(user = user))
                    return response_400(response_data)
                elif user.is_verified == False:
                    response_data.update(UserApiV1Msg.userNotVerified(user = user))
                    return response_400(response_data)
                elif user.is_active == False:
                    response_data.update(UserApiV1Msg.userInActive(user = user))
                    return response_400(response_data)
                # check the requested user already associated with org
                try:
                    emp = BMdl.OrgEmp.objects.get(user=user,org=request.data['org'])
                    response_data.update(BApiV1Msg.OrgEmpMsg.businessOrgEmpFound(emp))
                    return response_409(response_data)
                except BMdl.OrgEmp.DoesNotExist:
                    pass
                serializer = BSrl.AddOrgEmpSerializer(data=request.data, context={'user': user})
                if serializer.is_valid():
                    serializer.save()
                    new_org_emp = serializer.data
                    response_data['org_emp'] = serializer.data
                    response_data['message'] = BApiV1Msg.OrgEmpMsg.businessOrgEmpAddSuccess(emp_user = user)
                    return response_201(response_data)
                return response_400(serializer.errors)
            # org is active and verified & employee is not manager of the org
            if org_emp != None and org_emp.is_manager == False:
                response_data.update(BApiV1Msg.OrgEmpMsg.businessOrgEmpNotMng(org = org_emp.org))
                return response_403(response_data)
            # org is active and not verified
            if org_emp != None and org_emp.org.is_verified == False:
                response_data.update(BApiV1Msg.businessOrgNotVerified(org = org_emp.org))
                return response_403(response_data)
            # employee is not part of organization
            response_data.update(BApiV1Msg.OrgEmpMsg.businessOrgEmpSelfNotFound())
            return response_403(response_data)
        response_data.update(TErr.badActionUser(request = request, \
                reason = 'orgEmpCreate?orgId_url={0}&body={1}'.format(kwargs['orgId'], request.data['org'])))
        return response_403(response_data)
    
    def list(self, request, *args, **kwargs):
        response_data = {}
        response_data['orgId'] = kwargs['orgId']
        org_emp = validateOrgEmpObj(request.user, kwargs['orgId'])
        if org_emp != None:
            employees = BMdl.OrgEmp.objects.filter(org=kwargs['orgId'])
            serializer = BSrl.OrgEmpListSerializer(employees, many=True)
            response_data['org_name'] = org_emp.org.name
            response_data['org_emp_list'] = serializer.data
            return Response(response_data, status=status.HTTP_200_OK)
        response_data.update(BApiV1Msg.OrgEmpMsg.businessOrgEmpSelfNotFound())
        return response_403(response_data)
