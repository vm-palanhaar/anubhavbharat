from indrail import models as IrMdl

from business.idukaan.api.v1 import api_srv as BApiV1Srv


def ValidateOrgShopEmp(user, shop, org):
    '''
    returning dictionary {'shop','emp','isMng'} else None
    '''
    org_emp = BApiV1Srv.ValidateOrgEmpObj(user=user, org=org)
    if org_emp != None:
        # query shop emp [to optimize shop query]
        try:
            shop_emp = IrMdl.ShopEmp.objects.get(org_emp=org_emp, shop=shop)
        except IrMdl.ShopEmp.DoesNotExist:
            shop_emp = None
        # find shop from shop_emp query result [if null query shop]
        shop_obj = shop_emp.shop if shop_emp != None else None
        if shop_obj == None:
            try:
                ''' NEVER CHANGE FUNCTIONALITY
                query with org_emp.org to prevent override ir shop from others
                '''
                shop_obj = IrMdl.Shop.objects.get(id=shop, org=org_emp.org)
            except IrMdl.Shop.DoesNotExist:
                pass

        # emp is org's manager
        if org_emp.is_manager == True:
            return {
                'org' : org_emp.org,
                'shop' : shop_obj,
                'orgEmp' : org_emp,
                'shopEmp' : shop_emp,
                'isMng' : org_emp.is_manager,
            }
        elif org_emp.is_manager == False:
            if shop_emp != None:
                is_mng = True if shop_emp.is_manager != org_emp.is_manager else False
            else:
                is_mng = org_emp.is_manager
            return {
                    'org' : org_emp.org,
                    'shop' : shop_obj,
                    'orgEmp' : org_emp,
                    'shopEmp' : shop_emp,
                    'isMng' : is_mng,
                }
    return None

def ValidateShopObj(shop):
    return shop.is_active and shop.is_verified
