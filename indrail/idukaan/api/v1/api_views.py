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
                    response_data.update(IrApiV1Msg.AddShopMsg.addShopFoundFailed())
                    return response_409(response_data)
                except IrMdl.ShopLic.DoesNotExist:
                    pass
                serializer = IrSrl.AddShop_iDukaanSrl(data = request.data, context={
                            'user':request.user, 'org' : org_emp.org})
                if serializer.is_valid():
                    serializer.save()
                    response_data['ir_shop'] = serializer.data
                    response_data['message'] = IrApiV1Msg.AddShopMsg.addShopSuccess()
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
                response_data.update(IrApiV1Msg.ShopList.irOrgShopListEmptyMng())
                return response_400(response_data)
            # emp is not manager of organization -> only show associated shops
            emp_shops = IrMdl.ShopEmp.objects.filter(user = request.user, shop__org = kwargs['orgId'])
            if emp_shops.count() > 0:
                shop_list = []
                for emp_shop in emp_shops:
                    serializer = IrSrl.OrgShopList_iDukaanSrl(emp_shop.shop, context={'emp_manager':emp_shop.is_manager})
                    shop_list.append(serializer.data)
                response_data['ir_shops'] = shop_list
                return response_200(response_data)
            response_data.update(IrApiV1Msg.ShopList.irOrgShopListEmptyMng())
            return response_400(response_data)
        # employee is not part of organization
        response_data.update(BApiV1Msg.OrgEmpMsg.businessOrgEmpSelfNotFound())
        return response_403(response_data)

    def partial_update(self, request, *args, **kwargs):
        response_data = {}
        response_data['id'] = kwargs['shopId']
        if kwargs['shopId'] == str(request.data['id']):
            org_shop_emp = IrApiV1Srv.ValidateOrgShopEmp(user=request.user, shop=kwargs['shopId'], org=kwargs['orgId'])
            # only manager from org or shop are allowed to update
            if org_shop_emp != None and org_shop_emp['shop'] != None:
                if org_shop_emp['isMng'] == True:
                    serializer = IrSrl.UpdateShop_iDukaanSrl(org_shop_emp['shop'], data=request.data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        response_data['ir_shop'] = serializer.data
                        return response_200(response_data)
                    return response_400(serializer.errors)
                response_data.update(IrApiV1Msg.ShopEmpMsg.irOrgShopEmpNotMng(shop=org_shop_emp['shop']))
                return response_400(response_data)
            if org_shop_emp != None and org_shop_emp['shop'] == None:
                if org_shop_emp['isMng'] == True:
                    response_data.update(IrApiV1Msg.ShopList.irOrgShopNotFound())
                    return response_400(response_data)
                response_data.update(IrApiV1Msg.ShopEmpMsg.irOrgShopEmpSelfNotFound())
                return response_400(response_data)
        response_data.update(TErr.badActionUser(request = request, \
                reason = 'irShopPartialUpdate?shopId_url={0}&body={1}'.format(kwargs['shopId'], request.data['id'])))
        return response_403(response_data)

    def retrieve(self, request, *args, **kwargs):
        response_data = {}
        response_data['id'] = kwargs['shopId']
        org_shop_emp = IrApiV1Srv.ValidateOrgShopEmp(user=request.user, shop=kwargs['shopId'], org=kwargs['orgId'])
        if org_shop_emp != None and org_shop_emp['shop'] != None:
            serializer = IrSrl.ShopInfo_iDukaanSrl(org_shop_emp['shop'])
            response_data['ir_shop'] = serializer.data
            return response_200(response_data)
        response_data.update(IrApiV1Msg.ShopEmpMsg.irOrgShopEmpSelfNotFound())
        return response_400(response_data)
