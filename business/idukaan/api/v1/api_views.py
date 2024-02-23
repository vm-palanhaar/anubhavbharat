from django.contrib.auth.mixins import PermissionRequiredMixin

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from knox.auth import TokenAuthentication

from anubhavbharat import api_errors as TErr

from business import models as BMdl
from business import serializers as BSrl
from business.idukaan.api.v1 import api_msg as BApiV1Msg
from business.idukaan.api.v1 import api_srv as BApiV1Srv

from users import models as UserMdl
from users import permissions as UserPerm
from users.api.v1 import api_msg as UserApiV1Msg


'''
---PROD---
1. list_org_types
2. add_org
3. list_org
4. org_info

---DEV---
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


@api_view(['GET'])
@permission_classes([IsAuthenticated, UserPerm.IsKyc])
@authentication_classes([TokenAuthentication])
def list_org_types(request):
    query = BMdl.OrgType.objects.filter(is_doc1=True)
    serializer = BSrl.ListOrgTypeSrl(query, many=True)
    return response_200({
            'orgTypeList' : serializer.data
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated, UserPerm.IsKyc])
@authentication_classes([TokenAuthentication])
def add_org(request):
    response_data = {}
    serializer = BSrl.AddOrgSrl(data=request.data, context={'user': request.user})
    if serializer.is_valid():
            serializer.save()
            response_data['orgData'] = serializer.data
            response_data['message'] = BApiV1Msg.AddOrgMsg.addOrgSuccess()
            return response_201(response_data)
            #TODO: validate the reg number w.r.t. doc type
    if 'regNo' in serializer.errors and serializer.errors['regNo'][0].code == 'unique':
            return response_409(BApiV1Msg.AddOrgMsg.addOrgFoundFailed())
    return response_400(serializer.errors)


@api_view(['GET'])
@permission_classes([IsAuthenticated, UserPerm.IsKyc])
@authentication_classes([TokenAuthentication])
def list_org(request):
    response_data = {}
    queryset = request.user.orgemp_set.all()
    if queryset.count() > 0:
        orgs = []
        for org_emp in queryset:
            response_map = BSrl.ListOrgSrl(org_emp.org).data
            response_map['isMng'] = org_emp.is_mng
            orgs.append(response_map)
        response_data['orgList'] = orgs
        response_data['isKyoFalseMsg'] = BApiV1Msg.OrgStatusMsg.businessOrgNotVerified()['error']['message']
        return Response(response_data, status=status.HTTP_200_OK)
    return response_400(BApiV1Msg.OrgListMsg.orgListFailed_NotFound())


@api_view(['GET'])
@permission_classes([IsAuthenticated, UserPerm.IsKyc])
@authentication_classes([TokenAuthentication])
def org_info(request):
    org_emp = BApiV1Srv.ValidateOrgEmpObj(user=request.user, org=request.data['orgId'])
    if org_emp != None:
        serializer = BSrl.OrgInfoSrl(org_emp.org)
        return response_200(serializer.data)
    return response_403(BApiV1Msg.OrgEmpMsg.businessOrgEmpSelfNotFound())


class OrgEmpApi(viewsets.ViewSet, PermissionRequiredMixin):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, UserPerm.IsKyc]

    def create(self, request, *args, **kwargs):
        response_data = {}
        response_data['orgId'] = kwargs['orgId']
        # validate org_id from URI and request body
        if kwargs['orgId'] == request.data['org']:
            org_emp = BApiV1Srv.ValidateOrgEmpObj(user=request.user, org=kwargs['orgId'])
            # org is active and verified & employee is manager of the org
            if org_emp != None and BApiV1Srv.ValidateOrgObj(org=org_emp.org) and org_emp.is_mng:
                # check the requested user exists in users profile
                try:
                    user = UserMdl.User.objects.get(username = request.data['user'])
                except UserMdl.User.DoesNotExist:
                    response_data.update(UserApiV1Msg.usernameUserNotFound())
                    return response_400(response_data)
                if user.is_active == False and user.is_kyc == False:
                    response_data.update(UserApiV1Msg.userInActiveNotVerified(user = user))
                    return response_400(response_data)
                elif user.is_kyc == False:
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
                    response_data['newOrgEmpData'] = serializer.data
                    response_data['message'] = BApiV1Msg.OrgEmpMsg.businessOrgEmpAddSuccess(emp_user = user)
                    return response_201(response_data)
                return response_400(serializer.errors)
            # org is active and verified & employee is not manager of the org
            if org_emp != None and org_emp.is_mng == False:
                response_data.update(BApiV1Msg.OrgEmpMsg.businessOrgEmpNotMng(org = org_emp.org))
                return response_403(response_data)
            # org is active and not verified
            if org_emp != None and org_emp.org.is_kyo == False:
                response_data.update(BApiV1Msg.OrgStatusMsg.businessOrgNotVerified())
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
        org_emp = BApiV1Srv.ValidateOrgEmpObj(user=request.user, org=kwargs['orgId'])
        if org_emp != None:
            employees = BMdl.OrgEmp.objects.filter(org=kwargs['orgId'])
            serializer = BSrl.OrgEmpListSerializer(employees, many=True)
            response_data['orgEmpList'] = serializer.data
            return Response(response_data, status=status.HTTP_200_OK)
        response_data.update(BApiV1Msg.OrgEmpMsg.businessOrgEmpSelfNotFound())
        return response_403(response_data)
    
    def partial_update(self, request, *args, **kwargs):
        response_data = {}
        response_data['id'] = kwargs['orgEmpId']
        response_data['orgId'] = kwargs['orgId']
        # validate id from URI and request body
        if kwargs['orgEmpId'] == request.data['id']:
            org_emp = BApiV1Srv.ValidateOrgEmpObj(user=request.user, org=kwargs['orgId'])
            # org is active and verified & employee is manager of the org
            if org_emp != None and BApiV1Srv.ValidateOrgObj(org=org_emp.org) and org_emp.is_mng:
                try:
                    req_emp = BMdl.OrgEmp.objects.get(id = request.data['id'])
                except BMdl.OrgEmp.DoesNotExist:
                    response_data.update(BApiV1Msg.OrgEmpMsg.businessOrgEmpNotFound(org = org_emp.org))
                    return response_400(response_data)
                # check if user is update/delete self
                if request.user == req_emp.user:
                    response_data.update(BApiV1Msg.OrgEmpMsg.businessOrgEmpSelfUd(org = org_emp.org))
                    return response_400(response_data)
                serializer = BSrl.UpdateOrgEmpSerializer(req_emp, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    response_data['updatedOrgEmpData'] = serializer.data
                    response_data['message'] = BApiV1Msg.OrgEmpMsg.businessOrgEmpUpdateSuccess(emp_user = req_emp.user)
                    return response_200(response_data)
                return response_400(serializer.errors)
            # org is active and verified & employee is not manager of the org
            if org_emp != None and org_emp.is_mng == False:
                response_data.update(BApiV1Msg.OrgEmpMsg.businessOrgEmpNotMng(org = org_emp.org))
                return response_403(response_data)
            # org is active and not verified
            if org_emp != None and org_emp.org.is_kyo == False:
                response_data.update(BApiV1Msg.OrgStatusMsg.businessOrgNotVerified())
                return response_403(response_data)
            # employee is not part of organization
            response_data.update(BApiV1Msg.OrgEmpMsg.businessOrgEmpSelfNotFound())
            return response_403(response_data)
        response_data.update(TErr.badActionUser(request = request, \
                reason = 'orgEmpPartialUpdate?orgEmpId_url={0}&body={1}'.format(kwargs['orgEmpId'], request.data['id'])))
        return response_403(response_data)
    
    def destroy(self, request, *args, **kwargs):
        response_data = {}
        response_data['id'] = kwargs['orgEmpId']
        response_data['orgId'] = kwargs['orgId']
        # validate id from URI and request body
        if kwargs['orgEmpId'] == request.data['id']:
            org_emp = BApiV1Srv.ValidateOrgEmpObj(user=request.user, org=kwargs['orgId'])
            # org is active and verified & employee is manager of the org
            if org_emp != None and BApiV1Srv.ValidateOrgObj(org=org_emp.org) and org_emp.is_mng:
                try:
                    req_emp = BMdl.OrgEmp.objects.get(id = request.data['id'])
                except BMdl.OrgEmp.DoesNotExist:
                    response_data.update(BApiV1Msg.OrgEmpMsg.businessOrgEmpNotFound(org = org_emp.org))
                    return response_400(response_data)
                # check if user is update/delete self
                if request.user == req_emp.user:
                    response_data.update(BApiV1Msg.OrgEmpMsg.businessOrgEmpSelfUd(org = org_emp.org))
                    return response_400(response_data)
                response_data['message'] = BApiV1Msg.OrgEmpMsg.businessOrgEmpDeleteSuccess(emp_user = req_emp)
                req_emp.delete()
                return response_200(response_data)
            # org is active and verified & employee is not manager of the org
            if org_emp != None and org_emp.is_mng == False:
                response_data.update(BApiV1Msg.OrgEmpMsg.businessOrgEmpNotMng(org = org_emp.org))
                return response_403(response_data)
            # org is active and not verified
            if org_emp != None and org_emp.org.is_kyo == False:
                response_data.update(BApiV1Msg.OrgStatusMsg.businessOrgNotVerified())
                return response_403(response_data)
            # employee is not part of organization
            response_data.update(BApiV1Msg.OrgEmpMsg.businessOrgEmpSelfNotFound())
            return response_403(response_data)
        response_data.update(TErr.badActionUser(request = request, \
                reason = 'orgEmpDestroy?orgEmpId_url={0}&body={1}'.format(kwargs['orgEmpId'], request.data['id'])))
        return response_403(response_data)
