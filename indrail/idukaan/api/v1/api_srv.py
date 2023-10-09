from indrail import models as IrMdl

from business.idukaan.api.v1 import api_srv as BApiV1Srv


def ValidateOrgShopEmp(user, shop, org):
    '''
    returning dictionary {'shop','emp','isMng'} else None
    '''
    org_emp = BApiV1Srv.ValidateOrgEmpObj(user=user, org=org)
    # employee is org's manager
    if org_emp != None and org_emp.is_manager == True:
        try:
            return {
                'shop' : IrMdl.Shop.objects.get(id = shop),
                'emp' : org_emp,
                'isMng' : org_emp.is_manager
            }
        except IrMdl.Shop.DoesNotExist:
            return {
                'shop' : None,
                'emp' : org_emp,
                'isMng' : org_emp.is_manager
            }
    elif org_emp != None and org_emp.is_manager == False:
        try:
            shop_emp = IrMdl.ShopEmp.objects.get(user=user, shop=shop, shop__org=org)
            return {
                'shop' : shop_emp.shop,
                'emp' : shop_emp,
                'isMng' : shop_emp.is_manager
            }
        except IrMdl.Shop.DoesNotExist:
            return {
                'shop' : None,
                'emp' : org_emp,
                'isMng' : org_emp.is_manager
            }
    return None

def ValidateShopObj(shop):
    return shop.is_active and shop.is_verified
