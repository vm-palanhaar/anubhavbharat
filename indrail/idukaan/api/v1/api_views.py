from django.contrib.auth.mixins import PermissionRequiredMixin

from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from knox.auth import TokenAuthentication

from tourism import api_errors as TErr

from indrail import models as IrMdl
from indrail import serializers as IrSrl
from indrail.idukaan.api.v1 import api_msg as IrApiV1Msg
from indrail.idukaan.api.v1 import api_srv as IrApiV1Srv

from business import models as BMdl
from business import serializers as BSrl
from business.idukaan.api.v1 import api_msg as BApiV1Msg
from business.idukaan.api.v1 import api_srv as BApiV1Srv

from users import models as UserMdl
from users import permissions as UserPerm
from users.common.api.v1 import api_msg as UserApiV1Msg

'''
PROD
1. ShopApi
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
        response_data['org'] = kwargs['orgId']
        if kwargs['orgId'] == str(request.data['org']):
            org_emp = BApiV1Srv.ValidateOrgEmpObj(user=request.user, org=kwargs['orgId'])
            # org is active and verified & employee is manager of the org
            if org_emp != None and BApiV1Srv.ValidateOrgObj(org=org_emp.org) and org_emp.is_manager:
                # check the shop license no exists in ShopLic
                try:
                    IrMdl.ShopLic.objects.get(reg_no = request.data['lic_no'])
                    response_data.update(IrApiV1Msg.IrAddShopMsg.addShopFoundFailed())
                    return response_409(response_data)
                except IrMdl.ShopLic.DoesNotExist:
                    pass
                serializer = IrSrl.AddShop_iDukaanSrl(data = request.data, context={
                            'org_emp':org_emp, 'org' : org_emp.org})
                if serializer.is_valid():
                    serializer.save()
                    response_data['ir_shop'] = serializer.data
                    response_data['message'] = IrApiV1Msg.IrAddShopMsg.addShopSuccess()
                    return response_201(response_data)
                return response_400(serializer.errors)
            # org is active and verified & employee is not manager of the org
            if org_emp != None and org_emp.is_manager == False:
                response_data.update(BApiV1Msg.OrgEmpMsg.businessOrgEmpNotMng(org = org_emp.org))
                return response_403(response_data)
            # org is active and not verified
            if org_emp != None and org_emp.org.is_verified == False:
                response_data.update(BApiV1Msg.OrgStatusMsg.businessOrgNotVerified())
                return response_403(response_data)
            # employee is not part of organization
            response_data.update(BApiV1Msg.OrgEmpMsg.businessOrgEmpSelfNotFound())
            return response_403(response_data)
        response_data.update(TErr.badActionUser(request = request, \
                reason = 'irShopCreate?orgId_url={0}&body={1}'.format(kwargs['orgId'], request.data['org'])))
        return response_403(response_data) 

    def list(self, request, *args, **kwargs):
        response_data = {}
        response_data['org'] = kwargs['orgId']
        org_emp = BApiV1Srv.ValidateOrgEmpObj(user=request.user, org=kwargs['orgId'])
        # org is active and verified
        if org_emp != None and BApiV1Srv.ValidateOrgObj(org=org_emp.org):
            # if emp is manager -> show all ir shops associated with organization 
            if org_emp.is_manager:
                shops = IrMdl.Shop.objects.filter(org = kwargs['orgId'])
                if shops.count() > 0:
                    serializer = IrSrl.OrgShopList_iDukaanSrl(shops, many=True, 
                                                              context={'emp_manager':org_emp.is_manager})
                    response_data['ir_shops'] = serializer.data
                    return response_200(response_data)
                response_data.update(IrApiV1Msg.IrShopList.irOrgShopListEmptyMng())
                return response_400(response_data)
            # emp is not manager of organization -> only show associated shops
            emp_shops = IrMdl.ShopEmp.objects.filter(org_emp = org_emp)
            if emp_shops.count() > 0:
                shop_list = []
                for emp_shop in emp_shops:
                    serializer = IrSrl.OrgShopList_iDukaanSrl(emp_shop.shop, context={'emp_manager':emp_shop.is_manager})
                    shop_list.append(serializer.data)
                response_data['ir_shops'] = shop_list
                return response_200(response_data)
            response_data.update(IrApiV1Msg.IrShopList.irOrgShopListEmptyMng())
            return response_400(response_data)
        # employee is not part of organization
        response_data.update(BApiV1Msg.OrgEmpMsg.businessOrgEmpSelfNotFound())
        return response_403(response_data)

    def partial_update(self, request, *args, **kwargs):
        response_data = {}
        response_data['id'] = kwargs['shopId']
        if kwargs['shopId'] == str(request.data['id']):
            emp = IrApiV1Srv.ValidateOrgShopEmp(user=request.user, shop=kwargs['shopId'], org=kwargs['orgId'])
            # only manager from org or shop are allowed to update
            if emp != None and emp['shop'] != None:
                if emp['isMng'] == True:
                    serializer = IrSrl.UpdateShop_iDukaanSrl(emp['shop'], data=request.data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        response_data['ir_shop'] = serializer.data
                        return response_200(response_data)
                    return response_400(serializer.errors)
                response_data.update(IrApiV1Msg.IrShopEmpMsg.irOrgShopEmpNotMng(shop=emp['shop']))
                return response_400(response_data)
            if emp != None and emp['shop'] == None:
                if emp['isMng'] == True:
                    response_data.update(IrApiV1Msg.IrShopList.irOrgShopNotFound())
                    return response_400(response_data)
                response_data.update(IrApiV1Msg.IrShopEmpMsg.irOrgShopEmpSelfNotFound())
                return response_400(response_data)
            # variable r_emp is null [r_emp is no more associated with org]
            response_data.update(BApiV1Msg.OrgEmpMsg.businessOrgEmpSelfNotFound())
            return response_400(response_data)
        response_data.update(TErr.badActionUser(request = request, \
                reason = 'irShopPartialUpdate?shopId_url={0}&body={1}'.format(kwargs['shopId'], request.data['id'])))
        return response_403(response_data)

    def retrieve(self, request, *args, **kwargs):
        response_data = {}
        response_data['id'] = kwargs['shopId']
        r_emp = IrApiV1Srv.ValidateOrgShopEmp(user=request.user, shop=kwargs['shopId'], org=kwargs['orgId'])
        if r_emp != None and r_emp['shop'] != None:
            serializer = IrSrl.ShopInfo_iDukaanSrl(r_emp['shop'])
            response_data['ir_shop'] = serializer.data
            return response_200(response_data)
        if r_emp != None and r_emp['shop'] == None:
            if r_emp['isMng']:
                response_data.update(IrApiV1Msg.IrShopList.irOrgShopNotFound())
                return response_400(response_data)
            response_data.update(IrApiV1Msg.IrShopEmpMsg.irOrgShopEmpSelfNotFound())
            return response_400(response_data)
        response_data.update(BApiV1Msg.OrgEmpMsg.businessOrgEmpSelfNotFound())
        return response_400(response_data)
    

class ShopEmpApi(viewsets.ViewSet, PermissionRequiredMixin):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, UserPerm.IsVerified]

    def create(self, request, *args, **kwargs):
        response_data = {}
        response_data['shop_id'] = kwargs['shopId']
        # validate shop_id from URI and request body
        if kwargs['shopId'] == request.data['shop']:
            r_emp = IrApiV1Srv.ValidateOrgShopEmp(user=request.user, shop=kwargs['shopId'], org=kwargs['orgId'])
            # variable r_emp and shop is not null
            if r_emp != None and r_emp['shop'] != None:
                # r_emp is manager of org/shop and shop is active+verified
                if r_emp['isMng'] and IrApiV1Srv.ValidateShopObj(shop=r_emp['shop']):
                    # check the requested user exists in org emp
                    try:
                        org_emp = BMdl.OrgEmp.objects.get(id=request.data['org_emp'])
                    except BMdl.OrgEmp.DoesNotExist:
                        response_data.update(BApiV1Msg.OrgEmpMsg.businessOrgEmpNotFound(org = r_emp['org']))
                        return response_400(response_data)
                    # check the requested user exists in shop
                    try:
                        shop_emp = IrMdl.ShopEmp.objects.get(org_emp = org_emp)
                        response_data.update(IrApiV1Msg.IrShopEmpMsg.addIrShopEmpFound(user = org_emp.user, shop = r_emp['shop']))
                        return response_409(response_data)
                    except IrMdl.ShopEmp.DoesNotExist:
                        pass
                    serializer = IrSrl.AddShopEmp_iDukaanSrl(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        response_data['ir_shop_emp'] = serializer.data
                        response_data['message'] = IrApiV1Msg.IrShopEmpMsg.addIrShopEmpSuccess(emp_user = org_emp.user)
                        return response_201(response_data)
                    return response_400(serializer.errors)
                # r_emp is manager of org/shop and shop is not active/verified
                if r_emp['isMng'] and IrApiV1Srv.ValidateShopObj(shop=r_emp['shop']) == False:
                    response_data.update(IrApiV1Msg.IrShopStatusMsg.irShopNotVerified())
                    return response_403(response_data)
                # r_emp is not manager of org and shop
                if r_emp['isMng'] == False:
                    response_data.update(IrApiV1Msg.IrShopEmpMsg.irOrgShopEmpNotMng(shop = r_emp['shop']))
                    return response_403(response_data)
            # variable r_emp is not null and shop is null
            if r_emp != None and r_emp['shop'] == None:
                if r_emp['isMng']:
                    response_data.update(IrApiV1Msg.IrShopList.irOrgShopNotFound())
                    return response_400(response_data)
                response_data.update(IrApiV1Msg.IrShopEmpMsg.irOrgShopEmpSelfNotFound())
                return response_400(response_data)
            # variable r_emp is null [r_emp is no more associated with org]
            response_data.update(BApiV1Msg.OrgEmpMsg.businessOrgEmpSelfNotFound())
            return response_400(response_data)
        response_data.update(TErr.badActionUser(request = request, \
                reason = 'irShopEmpCreate?shopId_url={0}&body={1}'.format(kwargs['shopId'], request.data['shop'])))
        return response_403(response_data)

    def list(self, request, *args, **kwargs):
        response_data = {}
        response_data['shop_id'] = kwargs['shopId']
        response_data['org_id'] = kwargs['orgId']
        if 'Emp-List' in request.headers:
            if 'org' in request.headers['Emp-List'] or 'irshop' in request.headers['Emp-List']:
                r_emp = IrApiV1Srv.ValidateOrgShopEmp(user=request.user, shop=kwargs['shopId'], org=kwargs['orgId'])
                # variable r_emp is not null and shop is null [shop is not associated with org]
                if r_emp != None and r_emp['shop'] == None:
                    if r_emp['isMng']:
                        response_data.update(IrApiV1Msg.IrShopList.irOrgShopNotFound())
                        return response_400(response_data)
                    response_data.update(IrApiV1Msg.IrShopEmpMsg.irOrgShopEmpSelfNotFound())
                    return response_400(response_data)
                if r_emp != None and r_emp['org'] == None:
                # variable r_emp is null [r_emp is no more associated with org]
                    response_data.update(BApiV1Msg.OrgEmpMsg.businessOrgEmpSelfNotFound())
                    return response_400(response_data)
            # only exclude the shop emps
            if 'org' in request.headers['Emp-List'] and r_emp['isMng']:
                if r_emp != None and r_emp['shop'] != None:
                    org_emps = BMdl.OrgEmp.objects.filter(org = r_emp['org'])
                    shop_emps = IrMdl.ShopEmp.objects.filter(shop = r_emp['shop']).values_list('org_emp', flat=True)
                    emps = []
                    for org_emp in org_emps:
                        if org_emp.id not in shop_emps:
                            emps.append(BSrl.OrgEmpListSerializer(org_emp).data)
                    if len(emps) > 0:
                        response_data['org_name'] = r_emp['org'].name
                        response_data['org-shop_emp_list'] = emps
                        return response_200(response_data)
                    response_data.update(IrApiV1Msg.IrShopEmpMsg.addIrOrgShopEmpListDuplicate())
                    return response_409(response_data)
            # only incluse shop emps
            if 'irshop' in request.headers['Emp-List']:
                if r_emp != None and r_emp['shop'] != None:
                    shop_emps = IrMdl.ShopEmp.objects.filter(shop = r_emp['shop'])
                    serializer = IrSrl.ShopEmpList_iDukaanSrl(shop_emps, many=True)
                    response_data['ir_shop_emp_list'] = serializer.data
                    return response_200(response_data)
            else:
                response_data.update(TErr.badActionUser(request=request, reason='irShopEmpList?Emp-List=HeaderEmpty'))
                return response_403(response_data)
        response_data.update(TErr.badActionUser(request=request, reason='irShopEmpList?Emp-List=HeaderNotFound'))
        return response_403(response_data)

    def partial_update(self, request, *args, **kwargs):
        response_data = {}
        response_data['id'] = kwargs['empId']
        response_data['shop_id'] = kwargs['shopId']
        # validate id from URI and request body
        if kwargs['empId'] == request.data['id']:
            r_emp = IrApiV1Srv.ValidateOrgShopEmp(user=request.user, shop=kwargs['shopId'], org=kwargs['orgId'])
            if r_emp != None and r_emp['shop'] != None:
                if r_emp['isMng']:
                    try:
                        req_emp = IrMdl.ShopEmp.objects.get(id = request.data['id'])
                    except IrMdl.ShopEmp.DoesNotExist:
                        response_data.update(IrApiV1Msg.IrShopEmpMsg.irShopEmpNotFound(shop=r_emp['shop']))
                        return response_400(response_data)
                    # check if user is update/delete self
                    if req_emp.org_emp.user == request.user:
                        response_data.update(IrApiV1Msg.IrShopEmpMsg.irShopEmpSelfUd(shop=r_emp['shop']))
                        return response_400(response_data)
                    serializer = IrSrl.UpdateShopEmp_iDukaanSrl(req_emp, data=request.data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        response_data['ir_shop_emp'] = serializer.data
                        response_data['message'] = IrApiV1Msg.IrShopEmpMsg.irShopEmpUpdateSuccess(user = req_emp.org_emp.user)
                        return response_200(response_data)
                response_data.update(IrApiV1Msg.IrShopEmpMsg.irOrgShopEmpNotMng(shop = r_emp['shop']))
                return response_403(response_data)
            if r_emp != None and r_emp['shop'] == None:
                if r_emp['isMng']:
                    response_data.update(IrApiV1Msg.IrShopList.irOrgShopNotFound())
                    return response_400(response_data)
                response_data.update(IrApiV1Msg.IrShopEmpMsg.irOrgShopEmpSelfNotFound())
                return response_400(response_data)
            # variable r_emp is null [r_emp is no more associated with org]
            response_data.update(BApiV1Msg.OrgEmpMsg.businessOrgEmpSelfNotFound())
            return response_400(response_data)
        response_data.update(TErr.badActionUser(request = request, \
                reason = 'irShopEmpPartialUpdate?shopEmpId_url={0}&body={1}'.format(kwargs['empId'], request.data['id'])))
        return response_403(response_data)

    def destroy(self, request, *args, **kwargs):
        response_data = {}
        response_data['id'] = kwargs['empId']
        response_data['shop_id'] = kwargs['shopId']
        # validate id from URI and request body
        if kwargs['empId'] == request.data['id']:
            r_emp = IrApiV1Srv.ValidateOrgShopEmp(user=request.user, shop=kwargs['shopId'], org=kwargs['orgId'])
            if r_emp != None and r_emp['shop'] != None:
                if r_emp['isMng']:
                    try:
                        req_emp = IrMdl.ShopEmp.objects.get(id = request.data['id'])
                    except IrMdl.ShopEmp.DoesNotExist:
                        response_data.update(IrApiV1Msg.IrShopEmpMsg.irShopEmpNotFound(shop=r_emp['shop']))
                        return response_400(response_data)
                    # check if user is update/delete self
                    if req_emp.org_emp.user == request.user:
                        response_data.update(IrApiV1Msg.IrShopEmpMsg.irShopEmpSelfUd(shop=r_emp['shop']))
                        return response_400(response_data)
                    response_data['message'] = IrApiV1Msg.IrShopEmpMsg.irShopEmpDeleteSuccess(user=req_emp.org_emp.user, shop=r_emp['shop'])
                    req_emp.delete()
                    return response_200(response_data)
                response_data.update(IrApiV1Msg.IrShopEmpMsg.irOrgShopEmpNotMng(shop = r_emp['shop']))
                return response_403(response_data)
            if r_emp != None and r_emp['shop'] == None:
                if r_emp['isMng']:
                    response_data.update(IrApiV1Msg.IrShopList.irOrgShopNotFound())
                    return response_400(response_data)
                response_data.update(IrApiV1Msg.IrShopEmpMsg.irOrgShopEmpSelfNotFound())
                return response_400(response_data)
            # variable r_emp is null [r_emp is no more associated with org]
            response_data.update(BApiV1Msg.OrgEmpMsg.businessOrgEmpSelfNotFound())
            return response_400(response_data)
        response_data.update(TErr.badActionUser(request = request, \
                reason = 'irShopEmpDelete?shopEmpId_url={0}&body={1}'.format(kwargs['empId'], request.data['id'])))
        return response_403(response_data)
